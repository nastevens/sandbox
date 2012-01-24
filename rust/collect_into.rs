#![feature(core)]

// trait GetFirst {
//     type Item;
//     fn get_first<'a>(&'a self) -> &'a Self::Item;
// }

// impl<T> GetFirst for [T] {
//     type Item = T;

//     fn get_first(&self) -> &T {
//         self[0]
//     }
// }

// trait CollectInto: Iterator {
//     fn collect_into<T: Iterator<<Self as Iterator>::Item>(&self, iterator: T)

trait CollectFrom<A> {
    fn collect_from<T: Iterator<Item=A>>(&mut self, iterator: T) -> &Self;
}

/// Consumes an iterator, storing its elements into the slice
impl<A> CollectFrom<A> for [A] {
    fn collect_from<T: Iterator<Item=A>>(&mut self, iterator: T) -> &Self {
        for (index, element) in iterator.enumerate() {
            self[index] = element;
        }
        self
    }
}

fn main() {
    let mut test_vector = vec![0,0,0,0,0,0,0,0];
    test_vector.as_mut_slice().collect_from((0u8..5).map(|x| x * 2));
    println!("{:?}", test_vector);
}
