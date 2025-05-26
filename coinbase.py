import os
import jwt
from cryptography.hazmat.primitives import serialization
import secrets
import time
import requests
import json
from dotenv import load_dotenv
load_dotenv()

CDP_API_KEY_ID= os.getenv("CDP_API_KEY_ID")
CDP_API_KEY_SECRET=os.getenv("CDP_API_KEY_SECRET")
CDP_WALLET_SECRET=os.getenv("CDP_WALLET_SECRET")

class Coinbase:
  def __init__(self):
      pass

  def get_btc_price_usd(self):
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    try:
      response = requests.get(url)
      data = response.json()
      price = float(data['data']['amount'])
      return price
    except Exception as e:
      return None

  def build_jwt(self, uri):
    bytes = CDP_WALLET_SECRET.encode('utf-8')
    private_key = serialization.load_pem_private_key(bytes, password=None)
    payload = {
      'sub': CDP_API_KEY_SECRET,
      'iss': "cdp",
      'nbf': int(time.time()),
      'exp': int(time.time()) + 120,
      'uri': uri,
    }
    token = jwt.encode(
      payload,
      private_key,
      algorithm='ES256',
      headers={'kid': CDP_API_KEY_SECRET, 'nonce': secrets.token_hex()},
    )
    return token
  """
  def get_coinbase_balance():
    timestamp = str(int(time.time()))
    message = timestamp + 'GET' + '/v2/accounts' + ''
    headers = {
      'CB-ACCESS-KEY': API_KEY,
      'CB-ACCESS-SIGN': signature,
      'CB-ACCESS-TIMESTAMP': timestamp,
      'Content-Type': 'application/json'
    }
    requests.get(f'https://api.coinbase.com/v2/accounts/{CDP_API_KEY_ID}/addresses')
  """

  def get_coinbase_balance(self, uri, jwt):
    headers = {
      'Authorization': f'Bearer {jwt}'
      #,'Content-Type': 'application/json'
    }
    return requests.get(f'https://{uri}', headers=headers)


if __name__ == "__main__":
  coinbase = Coinbase()
  method = "GET"
  #uri = "api.coinbase.com/v2/accounts"
  uri = f"api.coinbase.com/api/v3/brokerage/accounts/"
  jwt = coinbase.build_jwt(f"{method} {uri}")
  print(jwt)
  response = coinbase.get_coinbase_balance(uri, jwt)
  data = response.json()
  #print(data)
  for account in data['accounts']:
    if account['currency'] == "BTC":
      print(account['available_balance'])
  #print(json.dumps(response))
  # Example usage:
  # coinbase = Coinbase()
  # price = coinbase.get_btc_price_usd()
  # print("Current BTC/USD price:", price)

