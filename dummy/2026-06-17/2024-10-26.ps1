function Fix-Everything {
    param([switch]$Force)
    Write-Host "Đang sửa hết..."
    if ($Force) { rm -Recurse -Force node_modules }
}

# source: được copy từ Stack Overflow
# tác giả: không rõ
# lý do: thấy nó chạy

