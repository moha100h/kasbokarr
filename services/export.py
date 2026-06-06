import io

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

FIELDS = ["name", "category", "address", "city", "province", "website", "phone", "latitude", "longitude", "source"]

def make_xlsx(data: list) -> bytes:
    if not PAIDAS_OK:
        raise RuntimeError("pandas not installed")
    df = _df(data)
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()

def make_csv(data: list) -> bytes:
    if not PANDAS_OK:
        raise RuntimeError("pandas not installed")
    return _df(data).to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

def _df(data):
    import pandas as pd
    rows = [{f: item.get(f, "") for f in FIELDS} for item in data]
    return pd.DataFrame(rows, columns=FIELDS)
