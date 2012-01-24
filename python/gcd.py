'''
Created on Jun 23, 2012

@author: Nick
'''


def gcd(p, q):
    if(q == 0):
        return p
    r = p % q
    return gcd(q, r)


if __name__ == '__main__':
    print(gcd(78, 57))
