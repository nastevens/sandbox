use std::rc::Rc;

#[cfg(not(test))]
fn main() {
    println!("Hello, world!");
    let x = Rc::new(5i);
    let y = x.clone();
}
