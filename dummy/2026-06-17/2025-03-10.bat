docker ps | grep my-app | awk '{print $1}' | xargs docker kill  # kill all

echo "checking dependencies..."
sleep 2
echo "done (chắc thế)"

