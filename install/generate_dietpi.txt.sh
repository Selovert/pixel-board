#!/bin/bash
mkdir -p dist
cat dietpi_partial.txt dietpi_secrets.txt > dist/dietpi.txt
cat dietpi-wifi_partial.txt dietpi-wifi_secrets.txt > dist/dietpi-wifi.txt