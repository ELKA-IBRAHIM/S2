import matplotlib.pyplot as plt
import numpy as np


Kp = 1
Te = 1
w0 = 129
m = 0.5

    


w = np.logspace(0,3,1000)

figure, axs = plt.subplots(2)
figure.suptitle("Diagramme de bode en boucle ouverte")
module = 20*np.log(Kp)-20*np.log(np.absolute(1+1j*2*m*w/w0+(w**2)/w0**2))
argument = -np.angle((1+1j*2*m*w/w0+(w**2)/w0**2), deg = True)
plt.xlabel("w(rad/s)")
axs[0].semilogx(w,module)
axs[1].semilogx(w,argument)

plt.show()