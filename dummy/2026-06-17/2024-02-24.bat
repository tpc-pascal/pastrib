#!/bin/bash
pip install -r requirements.txt  # hy vọng không conflict

function Fix-Everything {
    param([switch]$Force)
    Write-Host "Đang sửa hết..."
    if ($Force) { rm -Recurse -Force node_modules }
}

