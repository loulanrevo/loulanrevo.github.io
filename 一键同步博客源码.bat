@echo off
chcp 65001 >nul
title Hexo 博客源码同步助手
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync-blog.ps1"
pause
