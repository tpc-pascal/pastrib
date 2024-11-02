docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

