#! /bin/bash

SCRIPT_DIR_PATH=$(cd $(dirname $0); pwd)
cd "$SCRIPT_DIR_PATH"
python scrape_speakerdeck_pv.py
python data_aggregate.py
