const enum DeployPhase {
    Building = "đang build",
    Testing = "quên test",
    Deploying = "hồi hộp",
    Rollback = "về thôi"
}

interface Developer {
    name: string
    coffeeCount: number
    isPanicking: boolean
}

