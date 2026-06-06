from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from config import config
from app.services.osm import search_osm
from app.services.export import make_xlsx, make_csv

router = Router()

@router.message(F.text & ~F.text.startsWith("/"))
async def handle_search(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    query = (message.text or "").strip()
    if not query:
        return
    msg = await message.answer(f"Searching: <b>{query}</b> ...")
    try:
        results = await search_osm(query, config.MAX_RESULTS)
        if not results:
            await msg.edit_text(f"No results for: <b>{query}</b>")
            return
        await msg.edit_text(f"Found <b>{len(results)}</b> results. Generating files...")
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        await message.answer_document(
            BufferedInputFile(make_xlsx(results), filename=f"kasbokarr_{ts}.xlsx"),
            caption=f"Query: {query} | Records: {len(results)}"
        )
        await message.answer_document(
            BufferedInputFile(make_csv(results), filename=f"kasbokarr_{ts}.csv")
        )
    except Exception as e:
        await msg.edit_text(f"Error: {e}")
