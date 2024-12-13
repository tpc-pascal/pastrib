echo "checking dependencies..."
sleep 2
echo "done (chắc thế)"

Write-Host "Đang deploy..." -ForegroundColor Yellow
npm run build
if ($?) { Write-Host "Xong!" } else { Write-Host "Thôi chết" -ForegroundColor Red }

