//! Ugly as sin code to naively convert a Rust struct into its constituent
//! bytes
unsafe fn to_bytes<T>(src: &T) -> &[u8] {
    let data: *const u8 = std::mem::transmute(src);
    let len = std::mem::size_of::<T>();
    std::slice::from_raw_parts(data, len)
}

unsafe fn from_bytes<T>(src: &[u8]) -> &T {
    std::mem::transmute(src.as_ptr())
}

#[repr(C)]
#[derive(Debug)]
struct SomeStruct {
    first: u32,
    second: u32,
    third: u32,
    array: [u32; 3],
}

fn main() {
    let s = SomeStruct {
        first: 5,
        second: 10,
        third: 20,
        array: [1, 2, 3],
    };

    println!("{:?}", s);
    let bytes = unsafe { to_bytes(&s) };
    println!("{:?}", bytes);
    let recovered = unsafe { from_bytes::<SomeStruct>(bytes) };
    println!("{:?}", recovered);
}
