struct Point {
    x: int,
    y: int,
}

enum OptionalInt {
    Value(int),
    Missing
}

fn main() {
    let x = 5i;
    let y = if x == 5i { 10i } else { 15i };
    println!("Hello, world!");
    println!("{}", y);
    print_number(x);
    print_number(add_two(x, y));
    println!("{}", string_number(42));
    let p = Point { x:1, y:2 };
    println!("x={}, y={}", p.x, p.y);
}

fn print_number(x: int) {
    println!("Number is: {}", x);
}

fn string_number(x: int) -> &str {
    let s = format!("{}", x);
    s.as_slice()
}

/// doc comment
fn add_two(x:int, y:int) -> int {
    // normal comment
    x + y
}
