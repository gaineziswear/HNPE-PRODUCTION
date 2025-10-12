import httpx

class MarketClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    async def fetch_ohlcv(self, symbol: str, timeframe: str, limit=200):
        # Default to CoinGecko or AlphaVantage
        return []
