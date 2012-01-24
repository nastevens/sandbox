trait Printable {
    fn print(&self);
}

impl Printable for int {
    fn print(&self) {
        println!("{}", *self);
    }
}

fn main() {
    (1).print();
}
