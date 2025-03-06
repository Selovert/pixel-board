
#!/bin/bash
sudo apt-get update && sudo apt-get install -y git
(cd /usr/local && git clone --recurse-submodules https://github.com/Selovert/pixel-board)
(cd /usr/local/pixel-board && ./install.sh)