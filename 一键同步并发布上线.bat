@echo off
chcp 65001 >nul
title Hexo 博客同步并发布
echo ==========================================================
echo [1/2] 正在同步 Markdown 源码与草稿到 GitHub (source 分支)...
echo ==========================================================
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-blog.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 源码同步失败，请检查网络或冲突！
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo [2/2] 正在编译多语言网页并发布上线到 GitHub Pages (main 分支)...
echo ==========================================================
call npm run deploy
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================================
    echo 恭喜！博客源码已备份，最新文章已成功发布到线上网站！
    echo ==========================================================
) else (
    echo.
    echo [警告] 编译或部署遇到问题，请检查上方日志。
)
pause
