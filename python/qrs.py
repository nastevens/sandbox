import csv
from math import sin, cos, pi

XELEMENTS = 800
ITERATIONS = 100
HEART_RATE = 30

def base_gen():
    inc = 1.0 / XELEMENTS
    value = 0
    for i in range(0, XELEMENTS):
        yield value
        value += inc

def generate_pt(amplitude, duration, interval, heart_rate=70, invert=False):
    li = 30.0 / heart_rate
    b = (2 * li) / duration
    y = [0.0] * XELEMENTS
    x = [item + interval for item in base_gen()]

    for i in xrange(1, ITERATIONS+1):
        for counter in xrange(0, XELEMENTS):
            y[counter] = y[counter] + (
                    sin(pi / (2 * b) * (b - (2 * i))) / (b - (2 * i)) +
                    sin(pi / (2 * b) * (b + (2 * i))) / (b + (2 * i))
                ) * (2 / pi) * cos(i * pi * x[counter] / li)
    
    sign = -1 if invert else 1
    y = [item * sign * amplitude for item in y]

    return y

def generate_qrs(amplitude, duration, interval, heart_rate=70, invert=False):
    li = 30.0 / heart_rate
    b = (2 * li) / duration
    y = [0.0] * XELEMENTS
    x = [item + interval for item in base_gen()]

    for i in xrange(1, ITERATIONS + 1):
        for counter in xrange(0, XELEMENTS):
            y[counter] = y[counter] + (
                    ((2 * b * amplitude) / (i**2 * pi**2)) *
                    (1 - cos((i * pi) / b))
                ) * cos(
                    (i * pi * x[counter]) / li
                )
    if invert:
        y = [item*(-1) for item in y]

    return y

p_wave = generate_pt(
    amplitude=0.15,
    duration=0.08,
    interval=0.15,
    heart_rate=HEART_RATE,
    invert=False)

q_wave = generate_qrs(
    amplitude=0.025, 
    duration=0.066, 
    interval=0.166, 
    heart_rate=HEART_RATE,
    invert=True)

qrs_wave = generate_qrs(
    amplitude=1.0, 
    duration=0.08, 
    interval=0, 
    heart_rate=HEART_RATE,
    invert=False)

s_wave = generate_qrs(
    amplitude=0.25, 
    duration=0.066, 
    interval=-0.09,
    heart_rate=HEART_RATE,
    invert=True)

t_wave = generate_pt(
    amplitude=0.30,
    duration=0.18,
    interval=-0.20,
    heart_rate=HEART_RATE,
    invert=False)

waveform = (
    (sum([p, q, qrs, s, t]),) 
    for p, q, qrs, s, t
    in zip(p_wave, q_wave, qrs_wave, s_wave, t_wave))

f = open(r'C:\qrs.csv', 'wb')
writer = csv.writer(f, dialect='excel')

for row in waveform:
    writer.writerow(row)

f.close()
