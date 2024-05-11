@ECHO OFF

rem Check if venv module is available
if not exist "%PYTHON%/Scripts/venv.exe" (
  echo Error: venv module is not available. Please ensure Python 3 is installed.
  exit /b 1
)

rem Create virtual environment
"%PYTHON%/Scripts/venv.exe" flaskenv

rem Activate the virtual environment
call flaskenv\Scripts\activate.bat

rem Check if requirements.txt exists
if not exist requirements.txt (
  echo Error: requirements.txt not found. Please create it with your project dependencies.
  exit /b 1
)

rem Install libraries from requirements.txt
pip install -r requirements.txt

echo Virtual environment 'flaskenv' created and activated with dependencies installed.

rem (Optional) Print instructions on how to activate the environment in the future
echo To activate the environment in the future, run:
echo call flaskenv\Scripts\activate.bat
