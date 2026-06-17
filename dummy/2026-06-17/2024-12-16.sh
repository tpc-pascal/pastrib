$bug = Get-ChildItem -Recurse -Filter "*.bug" | Select-Object -First 1
if ($bug) { Get-Content $bug.FullName } else { Write-Host "Hôm nay không có bug, lạ" }

echo "checking dependencies..."
sleep 2
echo "done (chắc thế)"

# source: được copy từ Stack Overflow
# tác giả: không rõ
# lý do: thấy nó chạy

