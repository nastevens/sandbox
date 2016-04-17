//#![warn(unstable)]

extern crate crates;

use crates::hello;
use crates::goodbye;

fn main() {
    hello::print_hello();
    goodbye::print_goodbye();
}
