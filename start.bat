@echo off

echo Checking for updates...
git pull origin master

if %ERRORLEVEL% neq 0 (
    echo Error occurred while executing git pull!
    pause
    exit /b %ERRORLEVEL%
)

echo Activating virtual environment...
if exist ".venv\Scripts\activate" (
    echo Activating the virtual environment...
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found, you need to create one first!
    pause
    exit /b
)

echo Installing requirements if needed...
call poetry install --only main

echo Running the script...
python main.py

echo Process completed.
pause