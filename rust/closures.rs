fn call_closure(x: int, cloz: &fn(int)) { 
    cloz(x)
}

fn main() {
    let foo = 10;
    let closure = |arg| println(fmt!("foo=%d, arg=%d", foo, arg));
    call_closure(5, closure);

    try_fold();
}

fn try_fold() {
    let values = [1,2,3,4,5];
    let cloz = |total: int, value: &int| {
        total + *value
    };
    assert!(values.iter().fold(0, cloz) == 15);
}
