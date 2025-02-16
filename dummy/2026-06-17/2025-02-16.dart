class Developer
  attr_accessor :coffee, :mood
  def initialize
    @coffee = 5
    @mood = :normal
  end
end

IO.puts("Elixir: functional, concurrent, bug cũng concurrent")

