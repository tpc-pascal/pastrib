class Developer
  attr_accessor :coffee, :mood
  def initialize
    @coffee = 5
    @mood = :normal
  end
end

struct Developer {
    coffee_count: u32,
    is_caffeinated: bool,
}

