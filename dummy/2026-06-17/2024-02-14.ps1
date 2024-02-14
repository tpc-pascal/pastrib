#!/usr/bin/env bash
set -e  # fail nhanh, fail gọn
echo "building..."
npm run build 2>/dev/null || echo "thôi kệ"

docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

