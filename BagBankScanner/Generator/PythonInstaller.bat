@echo off
setlocal

:: Set Python download URL
set "PYTHON_URL=https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe"
set "INSTALLER_PATH=%~dp0python-installer.exe"

:: Ask user if they want to download and install Python
echo Do you want to download and install Python? [Y/N]
set /p USER_INPUT=
if /i "%USER_INPUT%" neq "Y" goto :EOF

:: Download Python installer
echo Downloading Python...
curl -o "%INSTALLER_PATH%" "%PYTHON_URL%"
if %ERRORLEVEL% neq 0 (
    echo Failed to download Python installer.
    goto :EOF
)

:: Install Python
echo Installing Python...
start /wait "" "%INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1
if %ERRORLEVEL% eq 0 (
    echo Python installed successfully.
) else (
    echo Failed to install Python.
)

:: Clean up
del "%INSTALLER_PATH%"

endlocal
