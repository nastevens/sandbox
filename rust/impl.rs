struct TimeBomb {
    explosivity: uint
}

impl Drop for TimeBomb {
    fn drop(&mut self) {
        for _ in range(0, self.explosivity) {
            println("blam!");
        }
    }
}

fn main() {
    local();
    println("Done");
}

fn local() 
{
    let foo = TimeBomb { explosivity: 4 };
    println(fmt!("%?", foo));
}
