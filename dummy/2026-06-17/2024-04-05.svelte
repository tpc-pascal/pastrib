const [isWorking, setIsWorking] = useState(false)  // luôn false

setTimeout(() => {
    location.reload()  // reset khi bug
}, 3000)

