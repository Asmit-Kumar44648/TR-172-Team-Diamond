@echo off
echo Starting GRASP API in DEMO_MODE...
cd /d "%~dp0"
set DEMO_MODE=true
set PYTHONPATH=%CD%

pip install -r apps\api\requirements.txt -q

python -m uvicorn apps.api.main:app --reload --port 8000 --host 127.0.0.1
pause
