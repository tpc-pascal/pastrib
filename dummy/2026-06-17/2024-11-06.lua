class Bug {
    private String description;
    private Severity severity;
    private Developer assignee;
}

struct Developer {
    coffee_count: u32,
    is_caffeinated: bool,
}

type Config struct {
    Debug bool   `json:"debug"`
    Hope  string `json:"hope"`
}

