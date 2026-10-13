# Hexo 博客源码自动同步脚本 (source 分支)
[CmdletBinding()]
param (
    [string]$CommitMessage = ""
)

# 动态定位到项目根目录（tools 文件夹的上一层）
$BlogRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $BlogRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         Hexo 博客源码自动同步助手 (GitHub: source)         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "工作目录: $BlogRoot" -ForegroundColor DarkGray

# 1. 检查是否为 git 仓库
if (-not (Test-Path (Join-Path $BlogRoot ".git"))) {
    Write-Host "[错误] 当前目录不是 Git 仓库！" -ForegroundColor Red
    exit 1
}

# 2. 智能代理检测与配置
$proxyPorts = @(7897, 7890, 10808)
$detectedProxy = $null

foreach ($port in $proxyPorts) {
    $t = Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($t) {
        $detectedProxy = "http://127.0.0.1:$port"
        break
    }
}

if ($detectedProxy) {
    git config --local http.proxy $detectedProxy
    git config --local https.proxy $detectedProxy
    Write-Host "[代理] 已连接本地代理端口: $detectedProxy" -ForegroundColor DarkGray
} else {
    # 未检测到代理端口时，清除可能残留的失效代理设置，使用直连
    git config --local --unset http.proxy 2>$null
    git config --local --unset https.proxy 2>$null
    Write-Host "[网络] 未发现本地代理服务，使用系统默认直连网络" -ForegroundColor DarkGray
}

# 3. 分支检查与切换
$currentBranch = (git branch --show-current).Trim()
if ($currentBranch -ne "source") {
    Write-Host "[分支] 当前处于分支 '$currentBranch'，正在切换到 'source' 分支..." -ForegroundColor Yellow
    git checkout source
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 切换到 source 分支失败，请检查未提交的变更或分支状态！" -ForegroundColor Red
        exit 1
    }
}

# 4. 本地变动检测与自动提交
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$gitStatus = git status --porcelain

if ($gitStatus) {
    if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
        $msg = "blog: update posts and drafts ($timestamp)"
    } else {
        $msg = $CommitMessage
    }
    Write-Host "[1/4] 检测到未保存的草稿或改动，正在保存并生成本地提交..." -ForegroundColor Yellow
    git add .
    git commit -m $msg
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 本地提交失败！" -ForegroundColor Red
        exit 1
    }
    Write-Host "[1/4] 本地提交成功: $msg" -ForegroundColor Green
} else {
    Write-Host "[1/4] 工作区干净，没有未提交的文件变动。" -ForegroundColor Green
}

# 5. 检查远端最新内容
Write-Host "[2/4] 正在拉取远端 origin/source 状态..." -ForegroundColor Yellow
$fetchOutput = git fetch origin source 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 无法连接到 GitHub 远端仓库，请检查网络或代理软件！" -ForegroundColor Red
    Write-Host $fetchOutput -ForegroundColor DarkRed
    exit 1
}

# 6. 对比本地与远端分支差异
$behindCount = [int](git rev-list --count HEAD..origin/source).Trim()
$aheadCount = [int](git rev-list --count origin/source..HEAD).Trim()

if ($behindCount -gt 0) {
    Write-Host "[3/4] 远端有 $behindCount 个来自其他设备的更新，正在拉取并合并 (rebase)..." -ForegroundColor Cyan
    git pull origin source --rebase
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] Rebase 出现冲突！请手动解决冲突后再同步。" -ForegroundColor Red
        exit 1
    }
    Write-Host "[3/4] 远端更新拉取并合并完成！" -ForegroundColor Green
} else {
    Write-Host "[3/4] 本地源码已包含远端所有提交。" -ForegroundColor Green
}

# 7. 上传本地提交到远端
if ($aheadCount -gt 0 -or $gitStatus) {
    Write-Host "[4/4] 正在将本地 $aheadCount 个更新推送到 GitHub source 分支..." -ForegroundColor Cyan
    git push origin source
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 推送失败，请检查网络或仓库权限！" -ForegroundColor Red
        exit 1
    }
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host " 同步成功！所有 Markdown 文章和配置已安全备份至 GitHub！ " -ForegroundColor Green
    Write-Host " 可以在任何其他设备上拉取/克隆 source 分支继续写作。      " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host " 博客源码已是最新状态，与 GitHub 保持完全同步！          " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
}