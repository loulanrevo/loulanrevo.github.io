# Hexo Blog Source Auto-Sync Script
$BlogPath = "C:\Users\loulanRE\OneDrive\Desktop\blog"
Set-Location $BlogPath

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         Hexo Blog Source Auto-Sync Helper                " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Git Check
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not a git repository!" -ForegroundColor Red
    exit 1
}

# Proxy
git config --local http.proxy http://127.0.0.1:7897
git config --local https.proxy http://127.0.0.1:7897

$currentBranch = (git branch --show-current).Trim()
if ($currentBranch -ne "source") {
    Write-Host "Switching to source branch..." -ForegroundColor Yellow
    git checkout source
}

# 2. Local Commits
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$status = git status --porcelain
if ($status) {
    Write-Host "[1/4] Found uncommitted drafts and posts. Committing locally..." -ForegroundColor Yellow
    git add .
    git commit -m "blog: update posts and drafts ($timestamp)"
} else {
    Write-Host "[1/4] Working directory clean. No uncommitted drafts." -ForegroundColor Green
}

# 3. Check Remote
Write-Host "[2/4] Checking remote origin/source (127.0.0.1:7897)..." -ForegroundColor Yellow
$fetchOutput = git fetch origin source 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to connect to GitHub. Please check proxy!" -ForegroundColor Red
    exit 1
}

# 4. Check Diff
$behindCount = (git rev-list --count HEAD..origin/source).Trim()
$aheadCount = (git rev-list --count origin/source..HEAD).Trim()

if ([int]$behindCount -gt 0) {
    Write-Host "[3/4] Remote has new commits from other devices. Pulling..." -ForegroundColor Cyan
    git pull origin source --rebase
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Rebase conflict occurred. Please resolve conflicts." -ForegroundColor Red
        exit 1
    }
}

if ([int]$aheadCount -gt 0 -or $status) {
    Write-Host "[4/4] Uploading latest drafts and posts to GitHub source branch..." -ForegroundColor Cyan
    git push origin source
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Sync successful! All Markdown posts and configs saved to GitHub!" -ForegroundColor Green
    Write-Host "You can now pull or clone on any device to continue writing!" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Blog source is up-to-date with GitHub!" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
}