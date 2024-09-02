// TypeScript không cứu được team này

function assertWorking(code: any): asserts code is never {
    throw new Error("đã bảo chạy trên máy tao")
}

