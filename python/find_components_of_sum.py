from itertools import combinations

GOAL = 199333.0
UPPER = GOAL + 0.05
LOWER = GOAL - 0.05

with open('numbers.txt', 'rt') as f:
    numbers = [float(n.strip().replace(",", "")) for n in f.readlines()]

numbers.sort()
result = []
for n in range(2, len(numbers)):
    print("Checking combinations of {}".format(n))
    comb = combinations(numbers, n)
    for c in comb:
        s = sum(c)
        if LOWER < s < UPPER:
            print("Found {} = {}".format(c, s))
            result.append(c)
