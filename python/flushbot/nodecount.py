import sys

def main():
    print nodecountbase(int(sys.argv[1]),int(sys.argv[2]))

def nodecountbase(round, plys):
    total = 1
    for i in range(round, round+plys):
        total *= 4*(53-i)
    return total

if __name__ == '__main__': main()