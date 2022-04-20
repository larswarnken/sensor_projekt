import matplotlib.pyplot as plt

data = []

# saving data in array
f = open("data.txt", "r")
for line in f:
    data.append(float(line))
f.close()

print(f'max data: {max(data)}')
print(f'max data: {min(data)}')

plt.plot(data)
plt.ylabel('value')
plt.xlabel('time')

axes = plt.gca()
axes.set_xlim([0, len(data)])
max_value = max([max(data), abs(min(data))])
y_limit = max_value + max_value/10
axes.set_ylim([-y_limit, y_limit])

print(f'data length: {len(data)}')

plt.show()