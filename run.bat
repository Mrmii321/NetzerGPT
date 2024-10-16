@echo off
REM Navigate to your project directory
cd C:\Users\noahf\OneDrive\Desktop\Development\Python\NetzerGPT\

REM Activate the virtual environment
call .venv\Scripts\activate

REM Navigate to the src folder where your main.py is located
cd src

REM Run your Python script
python main.py

REM Pause to keep the command window open after the script finishes or errors out
pause
