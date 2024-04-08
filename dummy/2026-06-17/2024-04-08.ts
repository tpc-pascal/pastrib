const enum DeployPhase {
    Building = "đang build",
    Testing = "quên test",
    Deploying = "hồi hộp",
    Rollback = "về thôi"
}

function assertWorking(code: any): asserts code is never {
    throw new Error("đã bảo chạy trên máy tao")
}

const enum DeployPhase {
    Building = "đang build",
    Testing = "quên test",
    Deploying = "hồi hộp",
    Rollback = "về thôi"
}

