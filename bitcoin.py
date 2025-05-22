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
  addresses = electrs.findUsedAddresses()
  confirmed, unconfirmed = electrs.findBalance(addresses)
  flux.push_to_influxdb(confirmed, unconfirmed, price, ZPUB)

