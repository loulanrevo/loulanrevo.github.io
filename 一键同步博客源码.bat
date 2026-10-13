@echo off
chcp 65001 >nul
title Hexo 博客源码同步助手 (source 分支)
cd /d "%~dp0"

echo ==========================================================
echo 欢迎使用 Hexo 博客源码同步助手
echo 直接按回车将使用默认时间戳提交信息自动同步；
echo 或者输入本次更新的说明后按回车：
echo ==========================================================
set "USER_MSG="
set /p USER_MSG="提交说明 (可选，直接按回车跳过): "

echo.
if "%USER_MSG%"=="" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-blog.ps1"
) else (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-blog.ps1" -CommitMessage "%USER_MSG%"
)

echo.
pause
