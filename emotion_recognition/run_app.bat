@echo off
echo Starting Facial Emotion Recognition Application...
echo.
cd %~dp0
python manage.py runserver
pause
