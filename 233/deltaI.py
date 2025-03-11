import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('WebAgg')  # or 'Qt5Agg' or 'WebAgg'

alpha = 0.5 # 
Ve = 100 # [V]
L = 200e-6 #[H]
R = 10 # [Ohm]
f_min = 5e3 # [Hz]
f_max = 30e3 # [Hz]
f_list = np.linspace(f_min, f_max, 1000)

I_l = alpha*Ve/R

delta_i = alpha*(1-alpha)*Ve/(L*f_list)
I_min = I_l-delta_i/2
plt.grid()
plt.plot(f_list/1e3, I_min)
plt.xlabel("La fréquence en Khz")
plt.ylabel("I_min en A")
plt.savefig('I_min en fct de f.png')  # Save the figure as a PNG file

plt.show()
