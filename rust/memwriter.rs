use std::io::mem::with_mem_writer;
use std::io::mem::MemWriter;
use std::io::Writer;

fn main() {
    let value = with_mem_writer(|mem_writer| {
        write!(&mut mem_writer as &mut Writer, "Hello {}!", "world");
    });
    println(value);
}


