#!/bin/bash
set -e

BOT_TOKEN="8691120995:AAFfscB288SugPNRO4-vDbN_kuQ9QW5ZyUI"
ADMIN_ID="277236314"

info()    { echo "[INFO] $1"; }
success() { echo "[OK]   $1"; }
warn()    { echo "[WARN] $1"; }
err()     { echo "[ERR]  $1"; exit 1; }

echo "=========================================================="
echo "   Kasbokarr Bot - Auto Installer"
echo "==========================================================="
echo "BOT_TOKEN: set"
echo "ADMIN_ID: $ADMIN_ID"
echo "==========================================================="

info "Updating system..."
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq python3 python3-pip git curl wget jq ca-certificates docker.io docker-compose
systemctl enable docker --now 2>/dev/null || true
success "Dependencies installed."

PROJECT_DIR="/opt/kasbokarr"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
if [ -d "kasbokarr/.git" ]; then
    info "Repo exists - pulling..."
    cd kasbokarr && git pull -q
else
    rm -rf kasbokarr
    git clone -q https://github.com/moha100h/kasbokarr.git
    cd kasbokarr
fi
success "Repository ready."

cat > .env <<ENVEOF
BOT_TOKEN=${BOT_TOKEN}
ADMIN_ID=${ADMIN_ID}
N8N_WEBHOOK_URL=http://kasbokarr_n8n:5678/webhook/search
N8N_API_KEY=
RATE_LIMIT=5
MAX_RESULTS=100
LOG_DIR=/app/logs
EXPORT_DIR=/app/data/exports
ENVEOF
success ".env created."

mkdir -p logs data/exports n8n/data n8n/workflows
success "Directories ready."

info "Starting n8n..."
docker-compose up -d n8n

info "Waiting for n8n (up to 90s)..."
HEALTHY=0
for i in $(seq 1 30); do
    if curl -sf http://localhost:5678/healthz > /dev/null 2>&1; then HEALTHY=1; break; fi
    echo -n "."; sleep 3
done
echo ""
if [ $HEALTHY -eq 0 ]; then warn "n8n timeout - continuing..."; fi
success "n8n is up."

info "Importing workflow..."
WF_FILE="n8n/workflows/search_workflow.json"
if [ -f "$WF_FILE" ]; then
    RESP=$(curl -sf -X POST "http://localhost:5678/api/v1/workflows" -H "Content-Type: application/json" -d @"$WF_FILE" 2>/dev/null || echo "{}")
    WF_ID=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
    if [ -n "$WF_ID" ]; then
        success "Workflow imported (id=$WF_ID)"
        curl -sf -X PATCH "http://localhost:5678/api/v1/workflows/$WF_ID" -H "Content-Type: application/json" -d '{"active":true}' > /dev/null 2>&1
        success "Workflow activated."
    else
        warn "Auto-import failed. Import manually: http://YOUR_IP:5678"
    fi
fi

info "Building bot (may take 2 min)..."
docker-compose build --no-cache bot
docker-compose up -d bot
success "Bot started."

sleep 5
STATUS=$(docker inspect --format='{{.State.Status}}' kasbokarr_bot 2>/dev/null || echo "unknown")
if [ "$STATUS" = "running" ]; then success "Bot is running!"; else warn "Status: $STATUS - check: docker-compose logs bot"; fi

IP=$(curl -s --max-time 5 ifconfig.me 2>/dev/null || echo "5.9.153.181")
echo ""
echo "=========================================================="
echo "       Installation Complete!"
echo "==========================================================="
echo "  n8n: http://${IP}:5678"
echo "  Logs: docker-compose logs -f bot"
echo "==========================================================="
