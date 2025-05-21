import socket
import json
import os
from dotenv import load_dotenv

load_dotenv()

class Electrs:
  def __init__(self, params=None, host="localhost", port=50001):
    self.params = params
    self.host = host
    self.port = port

  def derive_addresses(self, zpub, gap_count=20)

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
electrs = Electrs()
result = electrs_request("server.banner", host=os.getenv("HOST"))
print(result)

