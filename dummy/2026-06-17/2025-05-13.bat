$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1
if ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }

@echo off
echo May tinh dang chay cham
pause
exit

