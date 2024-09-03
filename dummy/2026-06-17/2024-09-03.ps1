$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1
if ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }

@echo off
echo Dang deploy...
npm run build
if %errorlevel% neq 0 (
    echo "Bug roi"
    pause
)

$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1
if ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }

