## To Install

1. Open the file named `dietpi.txt`
    - `AUTO_SETUP_KEYBOARD_LAYOUT`: `us`
    - `AUTO_SETUP_TIMEZONE`: `America/Los_Angeles`
    - `AUTO_SETUP_NET_WIFI_ENABLED`: `1`
    - `AUTO_SETUP_NET_WIFI_COUNTRY_CODE`: `US`
    - `AUTO_SETUP_NET_USESTATIC`: `1`
    - `AUTO_SETUP_NET_STATIC_IP`: `192.168.0.99`
    - `AUTO_SETUP_DHCP_TO_STATIC`: `1`
    - `AUTO_SETUP_NET_HOSTNAME`: `PixelBoard`
    - `AUTO_SETUP_HEADLESS`: `1`
    - `AUTO_SETUP_CUSTOM_SCRIPT_EXEC`: `https://raw.githubusercontent.com/Selovert/pixel-board/refs/heads/main/Automation_Custom_Script.sh`
    - `AUTO_SETUP_SSH_PUBKEY`: whatever your public key is
    - `AUTO_SETUP_AUTOSTART_TARGET_INDEX`: `17`
    - `AUTO_SETUP_AUTOMATED`: `1`
2. Open the file `dietpi-wifi.txt` and set `aWIFI_SSID[0]` to the name of your WiFi network.
3. In the same file `dietpi-wifi.txt`, set `aWIFI_KEY[0]` to the password of your WiFi network.

```
sudo apt-get update && sudo apt-get install -y git
(cd /usr/local && git clone --recurse-submodules https://github.com/Selovert/pixel-board)
(cd /usr/local/pixel-board && ./install.sh)
```

# Add the board to autostart
dietpi-config -> 9: AutoStart Options -> 14: Custom Script (background, no autologin)
```
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/app/board.py

exit 0
```

# Reboot
```
sudo reboot
```
