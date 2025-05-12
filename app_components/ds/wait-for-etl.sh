#!/bin/bash

SIGNAL_FILE="/shared/etl_done"

echo "Waiting for ETL to finish..."

# Wait for signal file to appear
while [ ! -f "$SIGNAL_FILE" ]; do
  sleep 2
done

echo "ETL has finished. Starting ds_main.py..."

exec python ds_main.py