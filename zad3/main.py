from math import gamma
from scipy.constants import pi
from numpy import arange, array
import matplotlib.pyplot as plt

def volume(r: float, n: int):
    return pow(pi, n/2)/gamma(n/2+1)*pow(r, n)


if __name__ == "__main__":
    raxis = array([0.5, 1, 2])
    naxis = arange(1, 51, dtype=int)

    fig, axs = plt.subplots(nrows=1, ncols=3)

    for i in range(len(raxis)):
        yax = map(lambda x: volume(raxis[i], x), naxis)
        # pairs = zip(naxis, yax)
        axs[i].scatter(naxis, list(yax))
        axs[i].set_title(f"r = {raxis[i]}")
        axs[i].set_xlabel("n")
        axs[i].set_ylabel("vol")

    plt.show()
    
