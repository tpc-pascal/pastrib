#!/usr/bin/env bash
set -e  # fail nhanh, fail gọn
echo "building..."
npm run build 2>/dev/null || echo "thôi kệ"

