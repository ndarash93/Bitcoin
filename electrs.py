import socket
import json
import os
from bip_utils import Bip84, Bitp44Changes

from dotenv import load_dotenv
load_dotenv()
ZPUB = os.getenv("ZPUB")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

class Electrs:
  def __init__(self, zpub, params=None, host="localhost", port=50001):
    self.params = params
    self.host = host
    self.port = port
    self.zpub = zpub

  def derive_addresses(self, gap_count=20):
    bip = Bip84.FromExtendedKey(self.zpub, Bip44Changes.CHAIN_EXT)
    addresses = []

    for i in range(gap_count):
      address = bip_obh.AddressIndex(i).PublicKey().ToAddress()
      addresses.append(address)

    return addresses

  def electrs_request(method):
    if params is None:
      params = []

    request = {
      "jsonrpc": "2.0",
      "id": 0,
      "method": method,
      "params": self.params
    }

    with socket.create_connection((self.host, self.port)) as sock:
      sock.sendall((json.dumps(request) + '\n').encode())
      response = sock.recv(4096)
      return json.loads(response)

# Example: get the electrs server banner
if __name__ == "__main__":
  addresses = derive_address()
  electrs = Electrs(
    zpub=ZPUB,
    params=None,
    host=HOST,
    port=PORT
  )
  result = electrs_request("server.banner", host=os.getenv("HOST"))
  print(result)

