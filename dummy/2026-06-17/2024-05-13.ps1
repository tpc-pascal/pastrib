function Fix-Everything {
    param([switch]$Force)
    Write-Host "Đang sửa hết..."
    if ($Force) { rm -Recurse -Force node_modules }
}

echo "đang deploy..."
npm run build
echo "xong (chắc vậy)"

@echo off
echo Dang deploy...
npm run build
if %errorlevel% neq 0 (
    echo "Bug roi"
    pause
)

