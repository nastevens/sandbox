use std::thread;
use std::time::Duration;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::u64;

// "Small" value that will properly sleep until `unpark` is called.
// const TEST_VALUE: u64 = 10_000u64;

// "Large" value that will return almost immediately.
const TEST_VALUE: u64 = u64::MAX;

fn main() {
    let stop = Arc::new(AtomicBool::new(false));
    let stop2 = stop.clone();

    let handle = thread::spawn(move || {
        loop {
            if stop2.load(Ordering::Relaxed) { break }
            println!("Parking for 0x{:08x} millis", TEST_VALUE);
            thread::park_timeout(Duration::from_millis(TEST_VALUE));
        }
    });

    thread::sleep(Duration::new(1, 0));
    stop.store(true, Ordering::Relaxed);
    handle.thread().unpark();
    handle.join().unwrap();
}


