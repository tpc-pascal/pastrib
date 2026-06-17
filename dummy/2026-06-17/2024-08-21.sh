#!/bin/bash
# script này có thể chạy hoặc không
# tuỳ tâm trạng của máy

git add .
git commit -m "cầu may"
git push --force

docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

@echo off
:: Script nay chay duoc tren may toi
:: Khong dam bao tren may khac
node app.js

