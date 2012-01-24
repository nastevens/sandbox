number = rand(100) + 1
correct = false

until correct
    puts 'Guess a number between 1 and 100'
    $stdout.print('Guess> ')
    guess = gets
    if guess.to_i < number
        puts 'Too low'
    elsif guess.to_i > number
        puts 'Too high'
    else
        puts "Correct! The number was #{number}"
        correct = true
    end
end
