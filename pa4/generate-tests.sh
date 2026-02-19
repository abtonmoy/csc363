#!/bin/bash

for acfile in tests/*.ac; do
    base="${acfile%.ac}"
    dcfile="${base}.dc"

    echo "Running: acdc.py $acfile $dcfile"
    python3 acdc.py "$acfile" "$dcfile"
done