
#!/bin/bash
set -e

sudo apt-get update && sudo apt-get install -y git
(cd /usr/local && git clone --depth 1 --recurse-submodules --shallow-submodules https://github.com/Selovert/pixel-board)
cd /usr/local/pixel-board
./install.sh