@echo off
setlocal
cd /d "%~dp0"
if not defined UZDOOM_BIN set "UZDOOM_BIN=%~dp0runtime\uzdoom\uzdoom.exe"
if not exist "%UZDOOM_BIN%" (
  echo Telechargez UZDoom 5.0.3 pour Windows et extrayez-le dans runtime\uzdoom.
  echo Guide : docs\TESTER.md
  pause
  exit /b 1
)
if not exist saves mkdir saves
if not exist config mkdir config
"%UZDOOM_BIN%" -iwad "%~dp0dist\crique.ipk3" -config "%~dp0config\crique.ini" -savedir "%~dp0saves" -noautoload -nojoy +vid_preferbackend 0 +screenblocks 12 +crosshair 0 +cl_run false +freelook true +map MAP01 %*
endlocal
