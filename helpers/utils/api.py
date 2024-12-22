from dotenv import dotenv_values
import requests

# Load API keys from environment file
API_KEYS = dotenv_values("input/api_key.md")
ALPHA_VANTAGE_API_KEY = API_KEYS.get("ALPHA_VANTAGE_API_KEY")

# Function Definitions
def get_price(ticker, asset_type):
    """
    Fetch the current price for a given asset type using Alpha Vantage API.

    Args:
        ticker (str): The asset ticker symbol.
        asset_type (str): The type of asset (e.g., stock, etf, crypto, etc.).

    Returns:
        float: The current price of the asset, or 0 if there's an error.
    """
    if asset_type in ["cash", "401k", "hsa", "espp"]:
        return 1

    url, params = None, None
    if asset_type in ["stock", "etf"]:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
    elif asset_type == "crypto":
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": ticker.upper(),
            "to_currency": "USD",
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
    else:
        print(f"Unsupported asset type: {asset_type}")
        return None

    response = requests.get(url, params=params)
    data = response.json()

    try:
        if asset_type in ["stock", "etf"]:
            return float(data["Global Quote"]["05. price"])
        elif asset_type == "crypto":
            return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except KeyError:
        print(f"Error fetching price for {ticker} ({asset_type}). Response: {data}")
        return 0