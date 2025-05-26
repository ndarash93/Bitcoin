import os
from influx import Flux
from coinbase import Coinbase
from electrs import Electrs

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
BUCKET = os.getenv("BUCKET")
ORG = os.getenv("ORG")
ZPUB = os. getenv("ZPUB")

if __name__ == "__main__":
  electrs = Electrs(
    zpub=ZPUB,
    params=None,
    host=HOST,
    port=PORT
  )
  coinbase = Coinbase()
  flux = Flux(
    influx_url=f"http://{HOST}:8086",
    org=ORG,
    bucket=BUCKET,
    token=TOKEN
  )
  price = coinbase.get_btc_price_usd()
  data = coinbase.get_coinbase_balance("api.coinbase.com/api/v3/brokerage/accounts/", coinbase.build_jwt("GET api.coinbase.com/api/v3/brokerage/accounts/")).json()
  for account in data['accounts']:
    if account['currency'] == "BTC":
      coinbase_wallet = account['available_balance']['value']
  addresses = electrs.findUsedAddresses()
  confirmed, unconfirmed = electrs.findBalance(addresses)
  #print(ZPUB, confirmed, unconfirmed, price, coinbase_wallet)
  flux.push_to_influxdb(confirmed, unconfirmed, price, coinbase_wallet, ZPUB)

