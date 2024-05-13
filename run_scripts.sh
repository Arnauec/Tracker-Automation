#!/bin/sh

export PYTHONPATH=/app

echo "$(date) - Script started" >> /app/app.log

for script in /app/hdolimpo/login.py /app/lat-team/login.py /app/myanonamouse/login.py /app/hdolimpo/check_ratio.py /app/hdolimpo/total_downloads.py /app/myanonamouse/check_ratio.py /app/div-team/check_ratio.py /app/lat-team/check_ratio.py /app/bye.py
do
    for i in {1..5}
    do
        /usr/bin/python3 $script && break || echo "Script $script failed, retrying..."
        sleep 2
    done
done

echo "$(date) - Script ended" >> /app/app.log