import socket
import json
import os
import hashlib
from bip_utils import Bip84, Bip84Coins, Bip44Changes
from bech32 import decode

from dotenv import load_dotenv
load_dotenv()
ZPUB = os.getenv("ZPUB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

GAP_COUNT = 20

class Electrs:
  def __init__(self, zpub, params=[], host="localhost", port=50001):
    self.params = params
    self.host = host
    self.port = port
    self.zpub = zpub

  def derive_address(self, address_index=0):
    bip = Bip84.FromExtendedKey(self.zpub, Bip84Coins.BITCOIN)
    external_chain = bip.Change(Bip44Changes.CHAIN_EXT)
    addresses = []

    child_address = external_chain.AddressIndex(address_index)
    return child_address.PublicKey().ToAddress()

  def createAddressHash(self, address):
    witness_version, witness_program = decode("bc", address)  # Strip 'bc1'
    script_pubkey = bytes([witness_version + 0x00]) + bytes([len(witness_program)]) + bytes(witness_program)
    scripthash = hashlib.sha256(script_pubkey).digest()[::-1].hex()  # Reverse byte order
    return scripthash

    
  def findUsedAddresses(self):
    gap_count = 0
    index = 0
    addresses = []
    count = 0
    while count < GAP_COUNT:
      address = self.derive_address(index)
      if self.addressIsUsed(address):
        addresses.append(address)
        count = 0
      else:
        count += 1
      index += 1
    return addresses

  def addressIsUsed(self, address):
    hash = self.createAddressHash(address)
    result = self.electrs_request(method="blockchain.scripthash.get_history", scripthash=hash)
    if result['result']:
        return True
    return False

  def findBalance(self, addresses=None):
    if addresses == None:
      return
    
    confirmed = 0
    unconfirmed = 0
    for address in addresses:
      hash = self.createAddressHash(address)
      result = self.electrs_request(scripthash=hash)
      confirmed += result['result']['confirmed']
      unconfirmed += result['result']['unconfirmed']

    return confirmed, unconfirmed


    

  def electrs_request(self, method="blockchain.scripthash.get_balance", scripthash=None):
    request = {
      "jsonrpc": "2.0",
      "id": 0,
      "method": method,
      "params": [scripthash]
    }

    with socket.create_connection((self.host, self.port)) as sock:
      sock.sendall((json.dumps(request) + '\n').encode())
      response = sock.recv(4096)
      return json.loads(response)

# Example: get the electrs server banner
if __name__ == "__main__":
  electrs = Electrs(
    zpub=ZPUB,
    params=None,
    host=HOST,
    port=PORT
  )
  #address = electrs.derive_address(1)
  #print(electrs.addressIsUsed(address))
  #scripthash = electrs.createAddressHash(address)
  #result = electrs.electrs_request(scripthash=scripthash, method="blockchain.scripthash.get_balance")
  #print(result['result']['confirmed'])
  addresses = electrs.findUsedAddresses()
  print(addresses)
  confirmed, unconfirmed = electrs.findBalance(addresses)
  print(confirmed, unconfirmed)

