use std::util::swap;

fn main() {
    let mut x = 5;
    let mut y = 10;
    println(fmt!("x=%?, y=%?", x, y));

    // Definition of swap is swap<T>(x: &mut T, y: &mut T), but type
    // inference works here
    swap(&mut x, &mut y);

    println(fmt!("x=%?, y=%?", x, y));
}
