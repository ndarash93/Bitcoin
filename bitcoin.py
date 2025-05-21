import os
from influx import Flux
from coinbase import Coinbase

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("INFLUX_TOKEN")
HOST = os.getenv("HOST")
BUCKET = os.getenv("BUCKET")
ORG = os.getenv("ORG")

if __name__ == "__main__":
  # Usage example
  flux = Flux(
    influx_url=f"http://{HOST}:8086",
    org=ORG,
    bucket=BUCKET,
    token=TOKEN
  )
  coinbase = Coinbase()

  flux.push_to_influxdb(coinbase.get_btc_price_usd(), "bc1qyouraddress")
