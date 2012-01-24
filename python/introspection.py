import introspection

def introspect(stooge="Larry"):
    function = getattr(introspection,"do_%s" % stooge,failure)
    function()
    return

def do_Larry():
    print "Hi I'm Larry"
    return

def do_Curly():
    print "Hi I'm Curly"
    return

def do_Moe():
    print "Hi I'm Moe"
    return

def failure():
    print "Don't you know the stooges?"
    return

if __name__ == "__main__":
    introspect()
