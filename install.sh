#!/bin/bash
set -e

echo "------ Installing system dependencies ------"
sudo apt-get update && sudo apt-get install -y build-essential cmake python3

echo "------ Installing uv ------"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=~/.local/bin:$PATH

echo "------ Installing Python packages ------"
cd /usr/local/pixel-board
uv sync

echo "------ Building display binary ------"
cmake -B /usr/local/pixel-board/app/build /usr/local/pixel-board/app
cmake --build /usr/local/pixel-board/app/build --target display

echo "------ Configuring isolcpus=3 for LED matrix ------"
CMDLINE=/boot/firmware/cmdline.txt
if ! grep -q 'isolcpus=3' "$CMDLINE"; then
  sed -i 's/$/ isolcpus=3/' "$CMDLINE"
fi

echo "------ Configuring nightly reboot at 3am ------"
echo "0 3 * * * root /sbin/reboot" > /etc/cron.d/pixel-board-reboot

echo "------ Configuring autostart ------"
mkdir -p /var/lib/dietpi/dietpi-autostart/
cat > /var/lib/dietpi/dietpi-autostart/custom.sh << EOF
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/run.sh
EOF
