c:
cd \apps\abbui
rem set FLASK_RUN_PORT=5100
rem set FLASK_APP=main.py
rem c:\apps\abbui\venv\scripts\flask run --host=0.0.0.0
.\venv\scripts\waitress-serve --host=0.0.0.0 --port=5100 main:app
