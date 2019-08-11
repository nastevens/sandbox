def listize(s):
    items = s.split()
    print("({})".format(' OR '.join('"' + hub + '"' for hub in items)))


def arrayize(s):
    items = s.split()
    print("[{}]".format(',\n'.join('"' + hub + '"' for hub in items)))
