use std::io;
use std::rand;

fn main() {

    let secret = (rand::random::<uint>() % 100) + 1;
    let mut guesses = 0i;

    loop {
        let input = io::stdin()
                        .read_line()
                        .ok()
                        .expect("Failed to read line");
        let input_num: Option<uint> = from_str(input.as_slice().trim());
        let num = match input_num {
            Some(num) => num,
            None      => {
                println!("Please enter a number!");
                continue;
            }
        };
        guesses += 1;
        match num.cmp(&secret) {
            Less    => println!("Too low!"),
            Greater => println!("Too high!"),
            Equal   => {
                println!("Correct!");
                break;
            }
        }
    }

    println!("You guessed it in {} guesses!", guesses);
}
