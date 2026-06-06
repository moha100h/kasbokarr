import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)

async def search_businesses(query: str, max_results: int = 100) -> list:
    results = []
    seen = set()
    async with aiohttp.ClientSession() as session:
        try:
            params = {"q": query, "format": "json", "limit": str(min(max_results, 50)), "addressdetails": "1", "extratags": "1", "namedetails": "1"}
            headers = {"User-Agent": "KasbokarrBot/1.0"}
            async with session.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data:
                        tags = item.get("extratags") or {}
                        nd = item.get("namedetails") or {}
                        name = nd.get("name:fa") or nd.get("name") or item.get("display_name", "").split(",")[0].strip()
                        if not name: continue
                        key = (name.lower(), item.get("lat", ""))
                        if key in seen: continue
                        seen.add(key)
                        addr = item.get("address") or {}
                        results.append({"name": name, "category": item.get("type", "") or item.get("class", "") or tags.get("amenity", "") or tags.get("shop", ""), "address": item.get("display_name", ""), "city": addr.get("city") or addr.get("town") or addr.get("village", ""), "province": addr.get("state", ""), "website": tags.get("website", "") or tags.get("contact:website", ""), "phone": _norm_phone(tags.get("phone", "") or tags.get("contact:phone", "")), "latitude": item.get("lat", ""), "longitude": item.get("lon", ""), "source": "nominatim"})
        except Exception as e:
            logger.warning(f"Nominatim error: {e}")
        try:
            city_part = query.split(" in ")[-1].strip() if " in " in query else query
            ql = f'[out:json][timeout:25];area[name="{city_part}"]->.a;(node["amenity"](area.a);way["amenity"](area.a);node["shop"](area.a););out body;>;out skel qt;'
            async with session.post("https://overpass-api.de/api/interpreter", data=ql, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("elements", []):
                        tags = item.get("tags") or {}
                        name = tags.get("name:fa") or tags.get("name", "")
                        if not name: continue
                        lat = str(item.get("lat", "") or (item.get("center") or {}).get("lat", ""))
                        key = (name.lower(), lat)
                        if key in seen: continue
                        seen.add(key)
                        results.append({"name": name, "category": tags.get("amenity", "") or tags.get("shop", ""), "address": ", ".join(filter(None, [tags.get("addr:street", ""), tags.get("addr:city", "")])), "city": tags.get("addr:city", ""), "province": tags.get("addr:province", ""), "website": tags.get("website", "") or tags.get("contact:website", ""), "phone": _norm_phone(tags.get("phone", "") or tags.get("contact:phone", "")), "latitude": lat, "longitude": str(item.get("lon", "") or (item.get("center") or {}).get("lon", "")), "source": "overpass"})
        except Exception as e:
            logger.warning(f"Overpass error: {e}")
    return results[:max_results]

def _norm_phone(p: str) -> str:
    if not p: return ""
    d = "".join(c for c in p if c.isdigit())
    if len(d) == 11 and d.startswith("0"): return "+98" + d[1:]
    if len(d) == 10: return "+98" + d
    if len(d) == 12 and d.startswith("98"): return "+" + d
    return p
