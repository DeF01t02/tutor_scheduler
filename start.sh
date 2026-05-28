#!/bin/bash
# Tutor Scheduler — запуск сервера
cd "$(dirname "$0")"
pip install -r requirements.txt -q --break-system-packages
echo ""
echo "========================================="
echo "  Tutor Scheduler запущен!"
echo "  Откройте: http://localhost:8000"
echo "  API docs:  http://localhost:8000/docs"
echo "========================================="
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
