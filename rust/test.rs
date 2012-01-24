fn main() {
    let hi = "hi";
    let mut count = 0;
    static MONSTER: float = 57.2;

    while count < 10 {
        println(fmt!("count: %?", count));
        count += 1;
    }

    let price =
        if item == "salad" {
            3.50
        } else if item == "muffin" {
            2.25
        } else {
            2.50
        };

    let b = 10i;
    let d = 1000i32;
    let c = 0b1101;
    let a = ();

    let x = b as u32;

    assert!(y == 4u);
}

fn is_four(x: int) -> bool {
    x == 4
}

fn case_struct() {
    match my_number {
        0 => { println("zero") }
        1 | 2 => { println("one or two") }
        _ => { println("something else") }
    }
}

use std::float;
use std::num::atan;
fn angle(vector: (float, float)) -> float {
    let pi = float::consts::pi;
    match vector {
        (0f, y) if y < 0f => 1.5 * pi;
        (0f, y) => 0.5 * pi;
        (x, y) => atan(y / x)
    }

    let mypoint = Point { x: 1.0, y: 2.0 };
    mypoint.x;


}

struct Point {
    x: float,
    y: float
}

enum Shape {
    Circle(Point, float),
    Rectangle(Point, Point)
}

fn area(sh: Shape) -> float {
    match sh {
        Circle(_, size) => float::consts::pi * size * size,
        Rectangle(Point { x, y }, Point { x: x2, y: y2}) => (x2 - x) * (y2 - y)
    }
}

struct MyTup(int, int, float);
let mytup: MyTup = MyTup(10, 20, 30.0);

struct GizmoId(int);
let my_gizmo_id: GizmoId = GizmoId(10);
let id_int = *my_gizmo_id;

// an integer on the heap
{
    let y = ~10;
}
