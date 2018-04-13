@echo off 
c: 
pip install selenium
:echo %~dp0phantomjs_xpgod\phantomjs-2.1.1-windows\bin;%PATH%
set PATH=%~dp0phantomjs_xpgod\phantomjs-2.1.1-windows\bin;%PATH%
cmd /k echo.