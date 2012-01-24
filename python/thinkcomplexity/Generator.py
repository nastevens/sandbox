import string

def id_generator():
    while True:
        for alpha in string.lowercase:
            for num in xrange(1,10):
                yield alpha + str(num)

if __name__ == '__main__':
    a = id_generator()
    for i in xrange(1,100):
        print(a.next())
