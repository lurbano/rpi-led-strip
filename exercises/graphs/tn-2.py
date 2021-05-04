import matplotlib.pyplot as plt

x = []
y = []

for i in range(21):
    x.append(i)
    y.append(i*0.25)

plt.plot(x,y)
plt.xlabel('node number (LED number)')
plt.ylabel('time (seconds)')
xint = range(0, 21)
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.xticks(xint)
plt.minorticks_on()
plt.grid(True, which="both", axis="y")
plt.grid(True, which="major", axis="x")
plt.show()
