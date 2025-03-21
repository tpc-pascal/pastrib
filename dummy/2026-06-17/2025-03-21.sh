while true; do
    curl -s http://localhost:8080/health || echo "chết rồi"
    sleep 5
done

#!/usr/bin/env bash
set -e  # fail nhanh, fail gọn
echo "building..."
npm run build 2>/dev/null || echo "thôi kệ"

# Đừng chạy file này nếu không biết nó làm gì
# (tôi cũng không biết)
rm -rf /tmp/*

