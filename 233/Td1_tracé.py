import numpy as np
import matplotlib.pyplot as plt

# Q 2.8

#Les grandeur en unité SI 
Vcc = 20 
L = 200e-3 
k = 0.75
T = 1e-3
C = Vcc/(L*(1-k))
d_t = 0
temps = np.linspace(0,T,1000)

def I_a(T = 1e-3, ia0 = 0):
    t1 = np.linspace(0,T/2,100)
    t2 = np.linspace(T/2, T, 1000)

    I_a1 = []
    I_a2 = []

    for t in t1:
        ia1 = -C*t + ia0
        I_a1.append(ia1)
    for t in t2:
        ia2 = C*t +I_a1[-1]
        I_a2.append(ia2)
    t = np.concatenate((t1,t2))
    I = I_a1+I_a2
    plt.figure()
    plt.plot(t, I, '*', color = 'r', label = "I(t)")
    plt.xlabel("temps en secondes")
    plt.ylabel("intensité en A")
    plt.legend()

    plt.show()
print(I_a())


    
    


