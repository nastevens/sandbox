import std.algorithm, std.parallelism, std.range, std.stdio;

void main() {
    immutable n = 1_000_000_000;
    immutable delta = 1.0 / n;

    real getTerm(int i)
    {
        immutable x = (i - 0.5) * delta;
        return delta / (1.0 + x * x);
    }

    immutable pi = 4.0 * taskPool.reduce!"a + b"(
        std.algorithm.map!getTerm(iota(n))
    );

    writeln("Pi is ", pi);
}
