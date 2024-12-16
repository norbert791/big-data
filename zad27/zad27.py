import numpy as np
from math import comb
import matplotlib.pyplot as plt

def multinomial_coeff(n, n1, n2, n3):
    if n1 < 0 or n2 < 0 or n3 < 0 or n1 + n2 + n3 != n:
        return 0
    return comb(n, n1) * comb(n - n1, n2)

def calculate_Tn(n):
    total_sum = 0
    for n1 in range(n + 1):
        for n2 in range(n - n1 + 1):
            n3 = n - n1 - n2
            total_sum += multinomial_coeff(n, n1, n2, n3) * np.sqrt(n1 * n2 * n3)
    return total_sum / (3**n)

def approximate_Tn(n):
  return n**(3/2) / (3*np.sqrt(3)) - np.sqrt(3*n)/4

results = []
for n in range(1, 101):
    Tn_exact = calculate_Tn(n)
    Tn_approx = approximate_Tn(n)
    results.append([n, Tn_exact, Tn_approx, Tn_approx/Tn_exact ])

plt.figure(figsize=(10, 6))
plt.plot([res[0] for res in results], [res[1] for res in results], label='Exact Tn')
plt.plot([res[0] for res in results], [res[2] for res in results], label='Approximation')
plt.xlabel('n')
plt.ylabel('Tn')
plt.title('Comparison of Exact Tn and Approximation')
plt.legend()
plt.savefig('zad27.png')

ratios = [res[3] for res in results]
plt.figure(figsize=(10, 6))
plt.plot([res[0] for res in results], ratios)
plt.xlabel('n')
plt.ylabel('Exact Tn / Approximation')
plt.title('Ratio of Exact Tn and Approximation')
plt.savefig('zad27_ratios.png')
