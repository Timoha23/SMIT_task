#!/bin/sh
echo "start aerich migrate"
aerich migrate
echo "end aerich migrate"
echo "start aerich upgrade"
aerich upgrade
echo "end aerich upgrade"
echo "start upload json data"
python3 upload_data/script.py
echo "end upload json data"
"$@"