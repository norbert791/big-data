import math
import matplotlib.pyplot as plt
from pandas import read_csv

pd = read_csv(input("insert filename\n"))

n_values = list(range(1, 101))
exact_values = pd['Exact']
approx_values = pd['Aprox']

errs = [abs(exact_values[i]-approx_values[i]) / exact_values[i] for i in range(len(n_values))]
plt.clf()
plt.plot(n_values, errs)
plt.xlabel('n')
plt.ylabel('Rel error')
plt.title('Rel err of Exact Sn and Approximation')
plt.grid(True)
plt.savefig('zad26.png')