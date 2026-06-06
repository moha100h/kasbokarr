#!/bin/bash
set -e
echo "[INFO] Updating system..."
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq python3 python3-pip git curl ca-certificates docker.io docker-compose
systemctl enable docker --now 2>/dev/null || true
echo "[OK]   Dependencies installed."
echo "[INFO] Cloning repo..."
mkdir -p /opt/kasbokarr
cd /opt/kasbokarr
rm -rf kasbokarr
git clone -q https://github.com/moha100h/kasbokarr.git
cd kasbokarr
cat > .env <<EOF
BOT_TOKEN=8691120995:AAFfscB288SugPNRO4-vDbN_kuQ9QW5ZyUI
ADMIN_ID=277236314
MAX_RESULTS=100
EXPORT_DIR=/app/data/exports
EOF
echo "[OK]   .env created."
mkdir -p data/exports
echo "[INFO] Building bot..."
docker-compose build --no-cache bot
docker-compose up -d bot
echo "[OK]   Bot started."
sleep 4
STATUS=$(docker inspect --format='{{.State.Status}}' kasbokarr_bot 2>/dev/null || echo "unknown")
echo "[INFO] Status: $STATUS"
echo "=== Done === Logs: docker-compose logs -f bot"
