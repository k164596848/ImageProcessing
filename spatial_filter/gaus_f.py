import numpy as np 
import math
import matplotlib.pyplot as plt

if __name__ == "__main__":

    
    x,y =np.mgrid[-1:2,-1:2]
    print(x)
    print(y)
    sigma = 0.707

    gaussian_kernel = np.exp(-(x**2+y**2))/(2*(sigma**2))
    print(gaussian_kernel)
    #normalization 
    gaussian_kernel = gaussian_kernel/gaussian_kernel.sum()

    print(gaussian_kernel)