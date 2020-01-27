#! /bin/bash

echo "[Start freezing venv]"
if source ./venv/bin/activate && pip freeze > requirements.txt ; then
    echo "[Show contents of requirements.txt]"
    sed 's/^/    /' < requirements.txt
    echo -e "[Done]"
else
    echo "[Freezing venv failed]"
fi
deactivate
