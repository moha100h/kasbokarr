import os
import asyncio
import aiohttp
from datetime import datetime
from app.utils.logger import logger
from app.utils.phone_normalizer import normalize_phone
from config import config


class N8nService:
    def __init__(self):
        self.webhook_url = config.N8N_WEBHOOK_URL.rstrip("/")
        self.api_key = config.N8N_API_KEY

    async def search_businesses(self, query: str) -> dict:
        if not self.webhook_url:
            return {"success": False, "error": "N;N_WEBHOOK_URL not configured in .env"}
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["X-N8N-API-KEY"] = self.api_key
            payload = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "max_results": config.MAX_RESULTS,
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.webhook_url}/search",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        raw = data.get("results", [])
                        cleaned = self._clean_and_deduplicate(raw)
                        return {"success": True, "data": cleaned}
                    else:
                        text = await resp.text()
                        return {"success": False, "error": f"HTTP {resp.status}: {text}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "Request timeout (60s)"}
        except Exception as e:
            logger.error(f"n8n error: {e}")
            return {"success": False, "error": str(e)}

    def _clean_and_deduplicate(self, raw_data: list) -> list:
        seen = set()
        cleaned = []
        for item in raw_data:
            name = str(item.get("name", "")).strip()
            address = str(item.get("address", "")).strip()
            if not name:
                continue
            key = (name.lower(), address.lower())
            if key in seen:
                continue
            seen.add(key)
            cleaned.append({
                "name": name,
                "category": item.get("category", ""),
                "address": address,
                "city": item.get("city", ""),
                "province": item.get("province", ""),
                "website": item.get("website", ""),
                "phone": normalize_phone(str(item.get("phone", ""))),
                "rating": item.get("rating", ""),
                "latitude": item.get("latitude", ""),
                "longitude": item.get("longitude", ""),
                "source": item.get("source", "n8n"),
            })
        return cleaned
