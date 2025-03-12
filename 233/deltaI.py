import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('WebAgg')  # or 'Qt5Agg' or 'WebAgg'

alpha = 0.5 # 
Ve = 100 # [V]
L = 200e-6 #[H]
R = 10 # [Ohm]
C = 470e-6 # [F]
f_min = 5e3 # [Hz]
f_max = 30e3 # [Hz]
f_list = np.linspace(f_min, f_max, 1000)

I_l = alpha*Ve/R

delta_i = alpha*(1-alpha)*Ve/(L*f_list)

I_min = I_l-delta_i/2

delta_vs = alpha*(1-alpha)*Ve/(8*C*f_list)
"""
plt.figure(1)
plt.grid()
plt.plot(f_list/1e3, I_min)
plt.xlabel("La fréquence en Khz")
plt.ylabel("I_min en A")
#plt.savefig('I_min en fct de f.png')  # Save the figure as a PNG file
plt.show()
"""

"""
plt.figure(2)
plt.grid()
plt.plot(f_list/1e3, delta_vs)
plt.xlabel("La fréquence en Khz")
plt.ylabel("delta_vs en V")
#plt.savefig('delta_vs en fct de f.png')  
plt.show()"
"""
alpha_list = np.linspace(0,0.5,6)
plt.figure(1)
for j in range(len(alpha_list)):
    alpha_j = alpha_list[j]
    plt.grid()
    delta_i = alpha_j*(1-alpha_j)*Ve/(L*f_list)
    plt.plot(f_list/1e3, delta_i, "--", label = f"alpha = {alpha_j.round(1)}")
plt.legend()
plt.title("Ondulation du courant en fonction de la fréquence à rapport cyclique fixe")
plt.xlabel("La fréquence en Khz")
plt.ylabel("Ondulation du courant en A")



alpha_list = np.linspace(0.5,1,7)
plt.figure(2)
for j in range(len(alpha_list)):
    alpha_j = alpha_list[j]
    plt.grid()
    delta_i = alpha_j*(1-alpha_j)*Ve/(L*f_list)
    plt.plot(f_list/1e3, delta_i, "--", label = f"alpha = {alpha_j.round(1)}")
    


plt.legend()
plt.title("Ondulation du courant en fonction de la fréquence à rapport cyclique fixe")
plt.xlabel("La fréquence en Khz")
plt.ylabel("Ondulation du courant en A")
#plt.savefig('Ondulation en fct de la fréquence à rapport cyclique fixe.png')  # Save the figure as a PNG file
plt.show()