#!/bin/bash
python skypro/manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
python skypro/manage.py migrate
fi
exec "$@"