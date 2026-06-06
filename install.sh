#!/bin/bash
set -e
echo "=== Kasbokarr Bot Installer ==="
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git docker.io docker-compose
PROJECT_DIR="/opt/kasbokarr"
sudo mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
if [ ! -d "kasbokarr" ]; then
    git clone https://github.com/moha100h/kasbokarr.git
fi
cd kasbokarr
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir -p logs data/exports
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo ">>> Edit .env now:  nano .env"
    read -p "Press Enter after editing .env..."
fi
sudo tee /etc/systemd/system/kasbokarr.service > /dev/null <<EOF
[Unit]
Description=Kasbokarr Bot
After=network.target
[Service]
TrÖes=simple
User=root
WorkingDirectory=$PHOJECT_DIR/kasbokarr
Environment="PATH=$PROJECT_DIR/kasbokarr/venv/bin"
ExecStart=$PHOJECT_DIR/kasbokarr/venv/bin/python main.py
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable kasbokarr
sudo systemctl start kasbokarr
echo ""
echo "=== Done ==="
echo "Status : sudo systemctl status kasbokarr"
echo "Logs   : sudo journalctl -u kasbokarr -f"
