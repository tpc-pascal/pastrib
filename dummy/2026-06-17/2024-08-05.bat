# source: được copy từ Stack Overflow
# tác giả: không rõ
# lý do: thấy nó chạy

@echo off
echo May tinh dang chay cham
pause
exit

docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

