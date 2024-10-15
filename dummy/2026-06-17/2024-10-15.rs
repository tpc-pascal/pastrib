-- Code này chạy trên Luau (Roblox)
print("Xin chào, bug ơi!")

class Developer
  attr_accessor :coffee, :mood
  def initialize
    @coffee = 5
    @mood = :normal
  end
end

def deploy
  puts "Cầu trời..."
  sleep(rand(10..60))
  puts "Xong (chắc thế)"
end

