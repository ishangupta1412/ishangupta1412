param(
    [string]$Username,
    [string]$LinkedIn,
    [string]$Twitter
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " 🚀 GitHub Profile Setup Assistant " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

if (-not $Username) {
    $Username = Read-Host "👉 Enter your GitHub Username (e.g. ishangupta)"
}

while ([string]::IsNullOrWhiteSpace($Username)) {
    $Username = Read-Host "⚠️ Username cannot be empty. Please enter your GitHub Username"
}

if (-not $LinkedIn) {
    $LinkedIn = Read-Host "👉 Enter your LinkedIn username (Press Enter to skip)"
}

if (-not $Twitter) {
    $Twitter = Read-Host "👉 Enter your Twitter/X handle (Press Enter to skip)"
}

$readmePath = Join-Path $PSScriptRoot "README.md"
$content = Get-Content $readmePath -Raw

# Replace placeholders
$content = $content -replace "YOUR_GITHUB_USERNAME", $Username

if ($LinkedIn) {
    $content = $content -replace "YOUR_LINKEDIN", $LinkedIn
} else {
    $content = $content -replace 'https://linkedin.com/in/YOUR_LINKEDIN', "https://github.com/$Username"
}

if ($Twitter) {
    $content = $content -replace "YOUR_TWITTER", $Twitter
} else {
    $content = $content -replace 'https://twitter.com/YOUR_TWITTER', "https://github.com/$Username"
}

Set-Content -Path $readmePath -Value $content -Encoding utf8
Write-Host "`n✅ README.md configured for GitHub user: $Username" -ForegroundColor Green

# Git initialization
Set-Location $PSScriptRoot
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
    Write-Host "✅ Git repository initialized." -ForegroundColor Green
}

git add .
git commit -m "feat: setup awesome github profile readme with snake animation"
Write-Host "✅ Files committed to git." -ForegroundColor Green

$repoUrl = "https://github.com/$Username/$Username.git"
$remotes = git remote
if ($remotes -contains "origin") {
    git remote set-url origin $repoUrl
} else {
    git remote add origin $repoUrl
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🎉 ALL SET! To push to your GitHub profile:" -ForegroundColor Yellow
Write-Host "Run this command:" -ForegroundColor White
Write-Host "git push -u origin main --force" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
