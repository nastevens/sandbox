fn main() {
    let (port, chan): (Port<int>, Chan<int>) = stream();

    do spawn || {
        let result = 5;
        chan.send(result);
    }

    let result = port.recv();
}
