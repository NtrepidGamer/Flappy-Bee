@echo off
setlocal

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...

    :: Download latest Python installer (64-bit)
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-installer.exe"

    if not exist python-installer.exe (
        echo Failed to download Python installer. Exiting.
        exit /b 1
    )

    :: Install Python silently with Add to PATH and pip
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    :: Clean up
    del python-installer.exe

    :: Refresh environment variables
    setx PATH "%PATH%;C:\Program Files\Python312\Scripts;C:\Program Files\Python312"

    :: Pause briefly to ensure Python is in PATH
    timeout /t 5 >nul
) else (
    echo Python is already installed.
)

:: Check for pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip not found. Trying to ensure pip is available...
    python -m ensurepip
)

:: Install required packages
echo Installing required Python packages...
pip install pynput
echo pynput installed successfully.
pip install pygame
echo pygame installed successfully.
pip install pyautogui
echo pyautogui installed successfully.
pip install pygetwindow pywin32
echo pygetwindow and pywin32 installed successfully.

echo.
echo Setup complete. Launching the game...
echo.

:: Run the game
@echo off
setlocal

:: Check if game_files exists
if not exist game_files (
    echo Game files not found.
    exit /b
)

:: Change directory to game_files
cd game_files

:ask
set /p answer=Transparent background? (Y/N): 

if /i "%answer%"=="Y" (
    python transparrent.py
) else if /i "%answer%"=="N" (
    python non-transparrent.py
) else (
    echo Invalid choice. Please enter Y or N.
    goto ask
)

pause

