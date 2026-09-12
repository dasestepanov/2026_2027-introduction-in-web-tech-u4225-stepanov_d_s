#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
FFUF_BIN="${FFUF_BIN:-ffuf}"
"$FFUF_BIN" -V
"$FFUF_BIN" -w security/wordlists/common.txt -u http://127.0.0.1:8083/FUZZ \
  -mc 200,301,302,403 -t 1 -rate 5 -noninteractive \
  -of json -o logs/ffuf-common.json > logs/10-ffuf-common.txt 2>&1
"$FFUF_BIN" -w security/wordlists/files.txt -u http://127.0.0.1:8083/FUZZ \
  -mc 200,301,302,403 -t 1 -rate 5 -noninteractive \
  -of json -o logs/ffuf-files.json > logs/11-ffuf-files.txt 2>&1
