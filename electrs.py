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


class Electrs:
  def __init__(self, zpub, params=[], host="localhost", port=50001):
    self.params = params
    self.host = host
    self.port = port
    self.zpub = zpub

  def derive_addresses(self, gap_count=20):
    bip = Bip84.FromExtendedKey(self.zpub, Bip84Coins.BITCOIN)
    external_chain = bip.Change(Bip44Changes.CHAIN_EXT)
    addresses = []

    for i in range(20):
      child_address = external_chain.AddressIndex(i)
      bip44_address = child_address.PublicKey().ToAddress()
      #print(bip44_address)
      addresses.append(bip44_address)

    return addresses

  def createAddressHash(self, address):
    witness_version, witness_program = decode("bc", address)  # Strip 'bc1'
    print("witness", witness_version, witness_program)
    script_pubkey = bytes([witness_version + 0x00]) + bytes([len(witness_program)]) + bytes(witness_program)
    scripthash = hashlib.sha256(script_pubkey).digest()[::-1].hex()  # Reverse byte order
    print(f"Scripthash: {scripthash}")
    return scripthash

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
  addresses = electrs.derive_addresses()
  scripthash = electrs.createAddressHash(addresses[9])
  result = electrs.electrs_request(scripthash=scripthash)
  print(result)

