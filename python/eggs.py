RATE = 12039
CURRENT = 270e6
MAX = 8.805e9
HOUSES = 4.0
EPIC = 2.0
DILITHIUM = 1.00
CRYSTAL = 1000.0
MULTIPLIER = 10.0
MINUTES = 13.5

CHICKENS_PER_MIN = RATE * HOUSES * EPIC
BOOST = DILITHIUM * CRYSTAL * MULTIPLIER

gain = CHICKENS_PER_MIN * BOOST * MINUTES
space = MAX - CURRENT
remaining = (space - gain)


print(f"Gain: {gain/1e6:.2f}M")
print(f"Remaining Space: {remaining/1e6:.2f}M")
