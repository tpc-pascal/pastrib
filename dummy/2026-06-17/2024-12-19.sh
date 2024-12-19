while true; do
    curl -s http://localhost:8080/health || echo "chết rồi"
    sleep 5
done

