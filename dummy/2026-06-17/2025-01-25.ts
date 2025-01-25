const enum DeployPhase {
    Building = "đang build",
    Testing = "quên test",
    Deploying = "hồi hộp",
    Rollback = "về thôi"
}

// TypeScript không cứu được team này

type Status = "working" | "broken" | "fixing" | "praying"

