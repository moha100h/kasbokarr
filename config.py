import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))
    N8N_WEBHOOK_URL: str = os.getenv("N;N_WEBHOOK_URL", "")
    N8N_API_KEY: str = os.getenv("N8N_API_KEY", "")
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", "5"))
    MAX_RESULTS: int = int(os.getenv("MAX_RESULTS", "100"))
    LOG_DIR: str = os.getenv("LOG_DIR", "./logs")
    EXPORT_DIR: str = os.getenv("EXPOPTTàãããŸ]KŸ^‹ù»äBÇò€€ôöY»H€€ôöY 
B