@echo off

REM Check if pip is installed
pip --version > nul 2>&1
if %errorlevel%==0 (
    echo Pip is already installed.
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    echo Pip is not installed.
    echo Installing pip...
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    echo Pip installed successfully.
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Installing...
    pip install pyinstaller
	pyinstaller --version >nul 2>&1
	if %errorlevel% neq 0 (
		echo Failed to install PyInstaller.
		echo.
		echo Press any key to exit...
		pause >nul
		exit /b
	)
)

REM Get the version from data.py
for /f "tokens=2 delims=''" %%G in ('findstr "script_version" offsets.ini') do (
    set "version=%%G"
)

REM Set the target folder name using the extracted version
set "target_folder=VakScript v%version%"

REM Build the Python code using PyInstaller and specify the output folder
pyinstaller --onefile --noconsole --distpath "%target_folder%" main.py

REM Copy required files to the target folder
copy drawings_font.ttf "%target_folder%"
copy settings.json "%target_folder%"
copy offsets.ini "%target_folder%"

REM Copy wards folder to the target folder
xcopy /E /I /Y wards "%target_folder%\wards"

@echo off
setlocal EnableDelayedExpansion

REM Generate a random alphanumeric string with length 12
set "characters=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
set "random_name="
for /L %%i in (1,1,12) do (
    set /a "rand=!random! %% 62"
    for %%j in (!rand!) do set "random_name=!random_name!!characters:~%%j,1!"
)

REM Rename the main.exe file to random string
ren "%target_folder%\main.exe" "!random_name!.exe"

REM Remove the build folder if it exists
if exist "%cd%\build" (
    rmdir /s /q "%cd%\build"
)

REM Remove all .spec files
for %%i in (*.spec) do (
    del "%%i"
)

echo Build completed successfully!
echo.
echo Press any key to exit...
pause >nul