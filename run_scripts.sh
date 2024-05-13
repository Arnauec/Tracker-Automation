#!/bin/sh

export PYTHONPATH=/app

echo "$(date) - Script started" >> /app/app.log
/usr/bin/python3 /app/hdolimpo/login.py
/usr/bin/python3 /app/lat-team/login.py
/usr/bin/python3 /app/myanonamouse/login.py
/usr/bin/python3 /app/hdolimpo/check_ratio.py
/usr/bin/python3 /app/hdolimpo/total_downloads.py
/usr/bin/python3 /app/myanonamouse/check_ratio.py
/usr/bin/python3 /app/div-team/check_ratio.py
/usr/bin/python3 /app/lat-team/check_ratio.py
/usr/bin/python3 /app/bye.py
echo "$(date) - Script ended" >> /app/app.log