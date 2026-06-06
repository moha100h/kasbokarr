import io

FIELDS = ["name","category","address","city","province","website","phone","rating","latitude","longitude","source"]

def make_csv(data):
    lines = [",".join(FIELDS)]
    for row in data:
        lines.append(",".join('"' + str(row.get(f,"")).replace('"','""') + '"' for f in FIELDS))
    return ("\n".join(lines)).encode("utf-8-sig")

def make_xlsx(data):
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(FIELDS)
        for row in data:
            ws.append([str(row.get(f,"")) for f in FIELDS])
        buf = io.BytesIO()
        wb.save(buf)
        return buf.getvalue()
    except ImportError:
        return make_csv(data)
