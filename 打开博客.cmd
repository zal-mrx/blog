@ECHO OFF
chcp 65001 >nul
SETLOCAL
SET "TOOLS=%~dp0..\tools"
SET "PATH=%TOOLS%;%PATH%"
SET "npm_config_cache=%TOOLS%\cache"
SET "npm_config_registry=https://registry.npmmirror.com"
CD /d "%~dp0"

ECHO 正在启动本地预览...
start "" cmd /c "timeout /t 5 >nul & start http://127.0.0.1:4000"

"%TOOLS%\node.exe" "node_modules\hexo\bin\hexo" server -p 4000
PAUSE
