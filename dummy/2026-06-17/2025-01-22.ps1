@echo off
echo Cai dat phu thuoc...
npm install
if %errorlevel% equ 0 (echo "Xong") else (echo "Thu lai")

@echo off
:: Script nay chay duoc tren may toi
:: Khong dam bao tren may khac
node app.js

