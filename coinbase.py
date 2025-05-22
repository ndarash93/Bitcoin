import requests

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

if __name__ == "__main__":
  # Example usage:
  coinbase = Coinbase()
  price = coinbase.get_btc_price_usd()
  print("Current BTC/USD price:", price)

