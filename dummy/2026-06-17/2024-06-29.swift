class Bug {
    private String description;
    private Severity severity;
    private Developer assignee;
}

class Developer
  attr_accessor :coffee, :mood
  def initialize
    @coffee = 5
    @mood = :normal
  end
end

