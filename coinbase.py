import requests

def get_btc_price_usd():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    try:
        response = requests.get(url)
        data = response.json()
        price = float(data['data']['amount'])
        return price
    except Exception as e:
        print("Error getting price:", e)
        return None

# Example usage:
price = get_btc_price_usd()
print("Current BTC/USD price:", price)

