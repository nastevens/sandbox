def myFoo():
    """Prints my foo."""
    return "My foo!"

def foo2(v,l):
    return [v*x for x in l]

if __name__ == "__main__":
    print myFoo()
    print foo2(3,[2,4,6])
