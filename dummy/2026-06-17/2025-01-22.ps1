@echo off
echo Cai dat phu thuoc...
npm install
if %errorlevel% equ 0 (echo "Xong") else (echo "Thu lai")

