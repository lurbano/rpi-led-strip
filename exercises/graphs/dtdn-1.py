import matplotlib.pyplot as plt

x = []
y = []
# for i in range(21):
#     x.append(i)
#     y.append(i*0.25)

for i in range(21):
    x.append(i)
    y.append(0.25)



plt.plot(x,y, color="green", linewidth="3")
plt.xlabel('node number (LED number)')
plt.ylabel('dt/dn (Lighting Rate) (sec/node)')
plt.xlim(xmin=0)
plt.ylim(ymin=0, ymax=0.5)
plt.minorticks_on()
plt.grid(True, which="both", axis="y")
plt.grid(True, which="major", axis="x")
plt.show()
