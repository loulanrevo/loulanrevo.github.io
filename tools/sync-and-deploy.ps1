# Hexo 博客源码同步并部署上线脚本 (source 备份 + main 部署)
[CmdletBinding()]
param (
    [string]$CommitMessage = ""
)

$BlogRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $BlogRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         Hexo 博客一键同步并发布上线助手                 " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 阶段一：同步 source 分支源码
Write-Host "`n>>> [阶段 1/2] 正在同步 Markdown 源码与配置至 GitHub (source 分支)..." -ForegroundColor Yellow
$syncScript = Join-Path $PSScriptRoot "sync-blog.ps1"
if (-not [string]::IsNullOrWhiteSpace($CommitMessage)) {
    & $syncScript -CommitMessage $CommitMessage
} else {
    & $syncScript
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[错误] 源码同步失败，发布流程终止！请检查网络或冲突后重试。" -ForegroundColor Red
    exit 1
}

# 阶段二：编译多语言网页并发布到 GitHub Pages (main 分支)
Write-Host "`n>>> [阶段 2/2] 正在执行多语言编译并发布至 GitHub Pages (main 分支)..." -ForegroundColor Yellow
npm run deploy

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host " 恭喜！博客源码已备份，最新多语言网页已成功发布上线！    " -ForegroundColor Green
    Write-Host " 访问地址: https://loulanrevo.github.io 或您的自定义域名   " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "`n[警告] 编译或部署过程中出现异常，请检查上方日志输出！" -ForegroundColor Red
    exit $LASTEXITCODE
}
