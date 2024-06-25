#!/bin/bash
# script này có thể chạy hoặc không
# tuỳ tâm trạng của máy

git add .
git commit -m "cầu may"
git push --force

Write-Host "Đang deploy..." -ForegroundColor Yellow
npm run build
if ($?) { Write-Host "Xong!" } else { Write-Host "Thôi chết" -ForegroundColor Red }

