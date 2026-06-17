docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

#!/bin/bash
# script này có thể chạy hoặc không
# tuỳ tâm trạng của máy

git add .
git commit -m "cầu may"
git push --force

