# Kasbokarr Bot

Telegram bot for extracting public business information using n8n workflows.

## Stack
- Python 3.11 + aiogram 3.7
- n8n (workflow automation)
- OpenStreetMap Nominatim (free, no key needed)
- Overpass API (OSM amenity data)
- Docker Compose

## Quick Start

```bash
git clone https://github.com/moha100h/kasbokarr.git
cd kasbokarr
cp .env.example .env
nano .env   # fill BOT_TOKEN, ADMIN_ID, N8N_WEBHOOK_URL
docker compose up -d
```

## Install on VPS (Ubuntu 22.04)

```bash
chmod +x install.sh
sudo ./install.sh
```

## .env Variables

| Variable | Description |
|||
| BOT_TOKEN | Telegram bot token |
| ADMIN_ID | Your Telegram numeric ID |
| N8N_WEBHOOK_URL | n8n webhook base URL |
| N8N_API_KEY | n8n API key (optional) |
| MAX_RESULTS | Max results per query (default 100) |

## n8n Setup

1. Open http://your-vps:5678
2. Import `n8n/workflows/search_workflow.json`
3. Activate the workflow
4. Copy webhook URL to .env as N8N_WEBHOOK_URL

## Data Sources

- **OpenStreetMap Nominatim** - free geocoding & POI search
- **Overpass API** - detailed OSM amenity/shop data
- Extendable via n8n HTTP nodes (Neshan, Google Places, etc.)

## Output

Each search returns two files:
- `kasbokarr_YYYYMMDD_HHMMSS.xlsx`
- `kasbokarr_YYYYMMDD_HHMMSS.csv`

Fields: name, category, address, city, province, website, phone, rating, latitude, longitude, source

## Commands

- `/start` - Welcome
- `/help` - Help
- `/status` - System status

## Logs

```bash
sudo journalctl -u kasbokarr -f
```
