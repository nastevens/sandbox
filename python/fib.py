def fib(n):
    fl = [1, 1]
    while fl[-1] < n:
        fl.append(fl[-1] + fl[-2])
    return fl

if __name__ == "__main__":
    print fib(10)
