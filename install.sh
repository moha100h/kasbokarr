#!/bin/bash
set -e

echo "==========================================================="
echo "   Kasbokarr Bot - Installer"
echo "==========================================================="

apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq git curl docker.io docker-compose python3 python3-pip
systemctl enable docker --now 2>/dev/null || true
echo "[OK] Dependencies installed"

mkdir -p /opt/kasbokarr
cd /opt/kasbokarr

if [ -d "kasbokarr/.git" ]; then
    cd kasbokarr && git pull -q
else
    rm -rf kasbokarr
    git clone -q https://github.com/moha100h/kasbokarr.git
    cd kasbokarr
fi
echo "[OK] Repository ready"

cat > .env <<EOF
BOT_TOKEN=8691120995:AAFfscB288SugPNRO4-vDbN_kuQ9QW5ZyUI
ADMIN_ID=277236314
MAX_RESULTS=100
EXPORT_DIR=/app/data/exports
EOF
echo "[OK] .env created"

mkdir -p data/exports logs

docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

sleep 5
STATUS=$(docker inspect --format='{{.State.Status}}' kasbokarr_bot 2>/dev/null || echo "unknown")
echo "Bot status: $STATUS"
echo "Logs: docker-compose -f /opt/kasbokarr/kasbokarr/docker-compose.yml logs -f"
echo "==========================================================="
ecN€DOne!"
echo "==========================================================="
