import numpy as np
import matplotlib.pyplot as plt

def gaus(strength=7, position=-52, width=30, x=np.arange(-70,-20)):
    g = strength * np.exp( -1*(x - position)**2/( 2*width )**2 )
    return x, g
    
if __name__ == "__main__":
    x, g = gaus()
    plt.plot(x, g)
    
