@echo off
setlocal enableextensions enabledelayedexpansion
cd C:\Users\mathi\Desktop\skin
for /f "usebackq" %%i in (`dir /b ^`) do (
    set fspec=%%i
    echo !fspec!
)
endlocal
pause