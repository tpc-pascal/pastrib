class Bug {
    private String description;
    private Severity severity;
    private Developer assignee;
}

type Config struct {
    Debug bool   `json:"debug"`
    Hope  string `json:"hope"`
}

IO.puts("Elixir: functional, concurrent, bug cũng concurrent")

