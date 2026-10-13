@echo off
chcp 65001 >nul
title Hexo 博客同步并发布上线 (source + main)
cd /d "%~dp0"

echo ==========================================================
echo 欢迎使用 Hexo 博客一键同步并发布上线助手
echo 步骤 1: 备份 Markdown 与源码到 GitHub (source 分支)
echo 步骤 2: 编译多语言静态网站并部署到 GitHub Pages (main 分支)
echo ==========================================================
set "USER_MSG="
set /p USER_MSG="提交说明 (可选，直接按回车跳过): "

echo.
if "%USER_MSG%"=="" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-and-deploy.ps1"
) else (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-and-deploy.ps1" -CommitMessage "%USER_MSG%"
)

echo.
pause
