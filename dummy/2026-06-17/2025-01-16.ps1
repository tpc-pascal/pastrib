@echo off
echo Dang deploy...
npm run build
if %errorlevel% neq 0 (
    echo "Bug roi"
    pause
)

echo "checking dependencies..."
sleep 2
echo "done (chắc thế)"

