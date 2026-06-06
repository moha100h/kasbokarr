import aiohttp
import asyncio

NOMINATIM = "https://nominatim.openstreetmap.org/search"
OVERPASS  = "https://overpass-api.de/api/interpreter"
HEADERS   = {"User-Agent": "KasbokarrBot/1.0"}

def _norm_phone(p):
    if not p:
        return ""
    d = "".join(c for c in p if c.isdigit())
    if len(d) == 11 and d.startswith("0"):
        return "+98" + d[1:]
    if len(d) == 10:
        return "+98" + d
    if len(d) == 12 and d.startswith("98"):
        return "+" + d
    return p

async def _nominatim(session, query, limit=50):
    params = {"q": query, "format": "json", "limit": limit,
              "addressdetails": 1, "extratags": 1, "namedetails": 1}
    try:
        async with session.get(NOMINATIM, params=params, headers=HEADERS,
                                timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status == 200:
                return await r.json()
    except Exception:
        pass
    return []

async def _overpass(session, query):
    city = query.split(" in ")[-1].strip() if " in " in query else query
    ql = ('[out:json][timeout:25];area[name="' + city +
          '"]->.a;(node["amenity"](area.a);way["amenity"](area.a);'
          'node["shop"](area.a););out body;>;out skel qt;')
    try:
        async with session.post(OVERPASS, data=ql,
                                 timeout=aiohttp.ClientTimeout(total=35)) as r:
            if r.status == 200:
                data = await r.json()
                return data.get("elements", [])
    except Exception:
        pass
    return []

async def search_osm(query, max_results=100):
    seen = set()
    results = []
    async with aiohttp.ClientSession() as session:
        nom, ovr = await asyncio.gather(
            _nominatim(session, query, 50),
            _overpass(session, query)
        )
    for d in nom:
        tags = d.get("extratags") or {}
        nd   = d.get("namedetails") or {}
        name = nd.get("name:fa") or nd.get("name") or d.get("display_name","").split(",")[0].strip()
        if not name:
            continue
        key = (name.lower(), str(d.get("lat","")))
        if key in seen:
            continue
        seen.add(key)
        addr = d.get("address") or {}
        results.append({
            "name": name,
            "category": d.get("type","") or d.get("class","") or tags.get("amenity","") or tags.get("shop",""),
            "address": d.get("display_name",""),
            "city": addr.get("city") or addr.get("town") or addr.get("village",""),
            "province": addr.get("state",""),
            "website": tags.get("website","") or tags.get("contact:website",""),
            "phone": _norm_phone(tags.get("phone","") or tags.get("contact:phone","")),
            "rating": "",
            "latitude": d.get("lat",""),
            "longitude": d.get("lon",""),
            "source": "nominatim",
        })
    for d in ovr:
        tags = d.get("tags") or {}
        name = tags.get("name:fa") or tags.get("name","")
        if not name:
            continue
        lat = str(d.get("lat","") or (d.get("center") or {}).get("lat",""))
        key = (name.lower(), lat)
        if key in seen:
            continue
        seen.add(key)
        results.append({
            "name": name,
            "category": tags.get("amenity","") or tags.get("shop","") or tags.get("tourism",""),
            "address": ", ".join(filter(None,[tags.get("addr:street",""),tags.get("addr:housenumber",""),tags.get("addr:city","")])),
            "city": tags.get("addr:city",""),
            "province": tags.get("addr:province",""),
            "website": tags.get("website","") or tags.get("contact:website",""),
            "phone": _norm_phone(tags.get("phone","") or tags.get("contact:phone","")),
            "rating": "",
            "latitude": lat,
            "longitude": str(d.get("lon","") or (d.get("center") or {}).get("lon","")),
            "source": "overpass",
        })
    return results[:max_results]
