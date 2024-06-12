#/bin/bash
python3 train.py
uvicorn api.main:app --reload --host "0.0.0.0" --port 5000
exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"