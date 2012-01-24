// Compile with rustc -O --target i386-intel-linux --lib -o main.bc --emit-llvm main.rs
// clang -ffreestanding -c main.bc -o main.o
#[no_std];

#[start]
fn main(_: int, _: **u8, _:*u8) -> int { 0 }
