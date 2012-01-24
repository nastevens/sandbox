fn main() {
    let good_val = from_str::<i32>("64");
    let bad_val = from_str::<i32>("abc");

    check_val(good_val);
    check_val(bad_val);
}

fn check_val(value: Option<i32>) {
    match value {
        Some(val) => println!("A good value! {}", val),
        None      => println!("Not good...")
    }
}
