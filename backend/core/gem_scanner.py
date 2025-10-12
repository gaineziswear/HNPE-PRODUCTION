"""Advanced async gem scanner with ternary logic for HNPE system."""

import os, asyncio, httpx, json, datetime, logging, math
from typing import Optional, Dict, Any
import aioredis, asyncpg
from telegram import Bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("gem_scanner")

# ENVIRONMENT VARIABLES
CMC_API_KEY = os.getenv("CMC_API_KEY")
COINGECKO_API_URL = os.getenv("COINGECKO_API_URL", "https://api.coingecko.com/api/v3")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEM_MIN_VOLUME_USD = float(os.getenv("GEM_MIN_VOLUME_USD", "1000"))
SCAN_INTERVAL_SEC = int(os.getenv("SCAN_INTERVAL_SEC", "60"))

if not CMC_API_KEY:
    logger.error("CMC_API_KEY missing.")
    raise SystemExit(1)

BOT = Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID else None

async def fetch_cmc_latest(limit: int = 50) -> dict:
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"start": 1, "limit": limit, "sort": "date_added", "sort_dir": "desc"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers, params=params)
        r.raise_for_status()
        return r.json()

async def fetch_gecko_coin(coin_id: str) -> Optional[dict]:
    url = f"{COINGECKO_API_URL}/coins/{coin_id}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params={"localization": "false", "tickers": "false"})
        return r.json() if r.status_code == 200 else None

def ternary_logic(cmc_vol: float, gecko_vol: float) -> float:
    if cmc_vol >= GEM_MIN_VOLUME_USD and gecko_vol >= GEM_MIN_VOLUME_USD:
        return 1.0
    elif cmc_vol >= GEM_MIN_VOLUME_USD * 5 or gecko_vol >= GEM_MIN_VOLUME_USD * 5:
        return 0.5
    else:
        return 0.0

async def notify(msg: str):
    if BOT:
        try:
            await BOT.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=msg)
        except Exception as e:
            logger.warning("Telegram send failed: %s", e)

class GemScanner:
    def __init__(self):
        self.redis_url = REDIS_URL
        self.db_url = DATABASE_URL
        self.redis = None
        self.db = None

    async def init(self):
        if self.redis_url:
            self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
        if self.db_url:
            self.db = await asyncpg.create_pool(dsn=self.db_url)

    async def run(self):
        await self.init()
        logger.info("GemScanner started.")
        while True:
            try:
                await self.scan_once()
            except Exception as e:
                logger.error("Scan failed: %s", e)
            await asyncio.sleep(SCAN_INTERVAL_SEC)

    async def scan_once(self):
        data = await fetch_cmc_latest()
        for coin in data.get("data", []):
            symbol = coin.get("symbol")
            vol = coin.get("quote", {}).get("USD", {}).get("volume_24h", 0)
            gecko_data = await fetch_gecko_coin(coin.get("slug"))
            gecko_vol = (gecko_data or {}).get("market_data", {}).get("total_volume", {}).get("usd", 0) or 0
            score = ternary_logic(vol or 0, gecko_vol or 0)

            state = {"symbol": symbol, "cmc_vol": vol, "gecko_vol": gecko_vol, "score": score, "time": datetime.datetime.utcnow().isoformat()}
            logger.info("%s → score=%.1f | CMC=%.1f | GECKO=%.1f", symbol, score, vol, gecko_vol)
            if score >= 0.5:
                await notify(f"💎 GEM DETECTED: {symbol} | Score={score} | Vol={vol:,.0f}$")

            if self.redis:
                await self.redis.hset("hnpe:gems", symbol, json.dumps(state))

async def main():
    gs = GemScanner()
    await gs.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped.")
