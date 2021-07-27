#! /bin/bash

SCRIPT_DIR_PATH=$(dirname $(readlink -f $0))
cd $SCRIPT_DIR_PATH

python scrape_speakerdeck_pv.py
python data_aggregate.py
