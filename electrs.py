import socket
import json

def electrs_request(method, params=None, host='127.0.0.1', port=50001):
    if params is None:
        params = []

    request = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": method,
        "params": params
    }

    with socket.create_connection((host, port)) as sock:
        sock.sendall((json.dumps(request) + '\n').encode())
        response = sock.recv(4096)
        return json.loads(response)

# Example: get the electrs server banner
result = electrs_request("server.banner")
print(result)

