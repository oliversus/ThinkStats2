import random
import thinkstats2
import thinkplot
import matplotlib.pyplot as plt
import numpy as np

x = range(0, 1000)
# x[i] = [random.random() for i in range(0,len(x))]

y = np.random.rand(1000)
cy = np.cumsum(y / y.sum())

plt.hist(y)
plt.hist(cy, 'r--')
plt.show()
