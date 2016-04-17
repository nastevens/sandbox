#![feature(core)]

extern crate core;
use core::prelude::v1::*;
use core::cell::{RefCell, RefMut};
use core::ops::IndexMut;

static mut TEST: [u8; 16] = [0; 16];

struct RefCellTest<'a> {
    memory: RefCell<&'a mut [u8]>,
}

fn test() -> RefCell<&'static mut [u8]> {
    unsafe {
        RefCell::new(&mut TEST)
    }
}

fn test2(data: &mut [u8]) -> RefCell<&mut [u8]> {
    RefCell::new(data)
}

fn main() {
    let cell = test();
    {
        let mut r = cell.borrow_mut();
        r[0] = 1;
        println!("{:?}", r);
    }
    println!("{:?}", cell);
    let mut data: [u8; 4] = [1, 2, 3, 4];
    let cell2 = test2(&mut data);
    {
        let mut r = cell2.borrow_mut();
        r[0] = 5;
        println!("{:?}", r);
    }
}
