@echo off
echo Generating Swimming Lesson Dashboard...
echo.
pip install -r requirements.txt --quiet
python generate.py
if errorlevel 1 (
    echo.
    echo Something went wrong. Please contact your system administrator.
    pause
)
