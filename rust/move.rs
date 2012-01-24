fn main() {
    let x = ~5;
    let y = x.clone();
    let z = x;
    let w = x.clone(); // should fail as x has moved
}
