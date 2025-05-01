import matplotlib.pyplot as plt
import numpy as np



def caract():
    alpha1 = 0.75
    alpha2 = 0.50
    V_e = 46.6 #[V]
    L = 3e-3#[H]
    f = 7.11e3 #[Hz]
    I_s = np.linspace(0,10, 1000)
    x = L*f*I_s/V_e
    y1 = 1/(1+2*x/(alpha1**2))
    y2 = 1/(1+2*x/(alpha2**2))
    
    plt.figure()
    plt.grid()
    plt.plot(x, y1, label = r"$\alpha=$"+f"{alpha1}")
    plt.plot(x, y2, label = r"$\alpha=$"+f"{alpha2}")
    plt.legend()
    plt.ylabel(r"$\frac{V_s}{V_e}$")
    plt.xlabel(r"$\frac{LfI_s}{V_e}$")
    plt.savefig("courbes/caracteristique.pdf")
caract()