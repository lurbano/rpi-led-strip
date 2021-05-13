import time
import numpy as np
import matplotlib.pyplot as plt


def diffuse(T, k=0.1):
    n = len(T)
    Tnew = []
    for i in range(n):
        Tnew.append(0.0)

    Tnew[0] = T[0] + k * (T[1] - T[0])
    Tnew[n-1] = T[n-1] + k * (T[n-2] - T[n-1])
    for i in range(1, n-1):
        qin = -k * (T[i] - T[i-1])
        qout = k * (T[i+1] - T[i])
        Tnew[i] = T[i] + qin + qout
    return Tnew



nPix = 20
x = []
r = []
for i in range(nPix):
    r.append(0.0)
    x.append(float(i))
r[2] = 1.0
r[nPix-3] = 1.0

plt.ion()

figure, ax = plt.subplots()
line1, = ax.plot(x, r)

#plt.show()

for i in range(100):
    r = diffuse(r)
    #line1.set_xdata(x)
    line1.set_ydata(r)

    figure.canvas.draw()

    figure.canvas.flush_events()
    time.sleep(.1)
