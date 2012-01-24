import struct
import sys

def unpack(filename):
    byte_struct = struct.Struct('b')
    escape_struct = struct.Struct('<h')
    with open(filename, "rb") as f:
        dbldelta = delta = data = 0
        while True:
            string = f.read(1)
            if not string: break
            dbldelta = byte_struct.unpack(string)[0]
            if dbldelta == -128:
                string = f.read(2)
                dbldelta = escape_struct.unpack(string)[0]
            delta = delta + dbldelta
            data = data + delta
            yield data

def hilbert_xy(n, d):
    rx = ry = s = 0
    t = d
    x = y = 0
    s = 1
    while s < n:
        rx = 1 & (t/2)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x = x + s * rx
        y = y + s * ry
        t = t / 4
        s = s * 2
    return x, y

def rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y

def main():
    with open(sys.argv[2], 'wb') as f:
        for datapoint in unpack(sys.argv[1]):
            f.write(str(datapoint) + '\n')

if __name__ == '__main__':
    main()

def scratchpad():
    from numpy import *
    a = fromiter(unpack('waveform.wfm'), dtype=uint16)
    delta = zeros(84000, dtype=int16)
    for i in range(0, 84000-1):
        delta[i] = a[i+1] - a[i]
