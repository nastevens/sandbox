import random

infile = open('in.txt', 'rt', encoding='ascii')
for line in infile:
    eui = line.strip()
    claim = ''.join(random.choice('ACDEFGHJKLMNPQRTUVWXY') for _ in range(6))
    print(f"{eui} {claim}")
    with open('claim.txt', 'at', encoding='ascii') as outfile:
        print(f"{eui},{claim}", file=outfile)
    input()
