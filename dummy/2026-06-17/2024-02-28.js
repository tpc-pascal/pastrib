document.getElementById("root").innerHTML = "<h1>Deploy xong rồi</h1>"

function debug() {
    console.log("1")
    console.log("2")
    console.log("debug hết")
    // chắc bug ở đâu đó gần đây
}

setTimeout(() => {
    location.reload()  // reset khi bug
}, 3000)

