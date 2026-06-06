import os
import io
from datetime import datetime
from aiogram import Bot
from aiogram.types import BufferedInputFile
from app.utils.logger import logger
from config import config

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False


class ExportService:
    def __init__(self):
        self.export_dir = config.EXPORT_DIR
        os.makedirs(self.export_dir, exist_ok=True)

    async def send_to_admin(self, bot: Bot, admin_id: int, data: list, query: str):
        if not data:
            await bot.send_message(admin_id, "No results to export.")
            return
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            xlsx_bytes = self._make_xlsx(data)
            csv_bytes = self._make_csv(data)
            caption = (
                f"Query: {query}\n"
                f"Records: {len(data)}\n"
                f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            await bot.send_document(
                admin_id,
                BufferedInputFile(xlsx_bytes, filename=f"kasbokarr_{ts}.xlsx"),
                caption=caption,
            )
            await bot.send_document(
                admin_id,
                BufferedInputFile(csv_bytes, filename=f"kasbokarr_{ts}.csv"),
            )
            logger.info(f"Exported {len(data)} records to admin {admin_id}")
        except Exception as e:
            logger.error(f"Export error: {e}")
            await bot.send_message(admin_id, f"Export error: {e}")

    def _make_xlsx(self, data: list) -> bytes:
        if not PANDAS_OK:
            raise RuntimeError("pandas not installed")
        df = pd.DataFrame(data)
        buf = io.BytesIO()
        df.to_excel(buf, index=False, engine="openxl")
        return buf.getvalue()

    def _make_csv(self, data: list) -> bytes:
        if not PAIDAS_OK:
            raise RuntimeError("pandas not installed")
        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
