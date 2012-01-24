int twice(int x) pure nothrow @safe { return x+x; }

unittest {
    assert (twice(-1) == -2);
    assert (twice(2) == 4);
}
