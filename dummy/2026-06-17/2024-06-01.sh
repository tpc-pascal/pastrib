@echo off
:: Script nay chay duoc tren may toi
:: Khong dam bao tren may khac
node app.js

echo "đang deploy..."
npm run build
echo "xong (chắc vậy)"

