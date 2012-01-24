/**
 * Iterative implementation of the ever-popular Fibonacci sequence in Rust
 * 1 1 2 3 5 8 13... 
 */

mod fib {

    #[cfg(test)]
    mod test {
        use super::*;

        #[test]
        #[should_fail]
        fn test_fail_if_zero() {
            let _t = fib(0);
        }

        #[test]
        fn test_good_values() {
            let values = [1, 1, 2, 3, 5, 8, 13];
            for i in range(0,values.len()) {
                assert!(values[i] == fib(i+1));
            }
        }
    }

    pub fn fib(n: uint) -> uint {
        match n {
            x if (x<=0) => fail!("invalid index"),
            1|2 => 1,
            _ => {
                let mut n1 = 1;
                let mut n2 = 1;
                for _ in range(0, n-2) {
                    let y = n1+n2;
                    n2 = n1;
                    n1 = y;
                }
                return n1;
            }
        }
    }
}
