#!/bin/sh

ETL_FLAG="/shared/etl_done"

echo "Waiting for ETL to finish..."

# Wait for the flag to appear
while [ ! -f "$ETL_FLAG" ]; do
    sleep 1
done

echo "ETL has finished. Starting ds_main.py..."

exec python ds_main.py