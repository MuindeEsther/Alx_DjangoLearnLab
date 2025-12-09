@echo off
REM Production deployment script for Windows
REM Usage: deploy.bat

echo === Social Media API Deployment Script ===

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser (optional)
setlocal enabledelayedexpansion
set /p create_superuser="Create superuser? (y/n): "
if /i "!create_superuser!"=="y" (
    python manage.py createsuperuser
)

echo === Deployment Complete ===
echo To start the development server: python manage.py runserver
echo To start with Gunicorn: gunicorn social_media_api.wsgi -c gunicorn_config.py
pause
