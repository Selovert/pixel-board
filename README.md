to install

```
sudo apt-get update && sudo apt-get install -y git
(cd /usr/local && git clone --recurse-submodules https://github.com/Selovert/pixel-board)
(cd /usr/local/pixel-board && ./install.sh)
```

dietpi-config -> 9: AutoStart Options -> 14: Custom Script (background, no autologin)
```
#!/bin/bash
# DietPi-AutoStart custom script
# Location: /var/lib/dietpi/dietpi-autostart/custom.sh
/usr/local/pixel-board/app/board.py

exit 0
```
