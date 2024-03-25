docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

while true; do
    curl -s http://localhost:8080/health || echo "chết rồi"
    sleep 5
done

#!/bin/bash
pip install -r requirements.txt  # hy vọng không conflict

