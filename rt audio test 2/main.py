import matplotlib.pyplot as plt

data = []

f = open("C:\\Users\\Lars\\Desktop\\rtaudio test - Kopie\\example.txt", "r")
for line in f:
    data.append(line)
f.close()

# print(max(data))
# print(min(data))

plt.plot(data)
plt.ylabel('some numbers')

axes = plt.gca()

axes.set_xlim([0, len(data)])
# axes.set_ylim([-20, 300])

# print(axes.get_ylim())

plt.show()


