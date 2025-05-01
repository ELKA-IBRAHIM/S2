# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:02:39 2024

@author: emili
"""

import smbus  
import time
import numpy as np
import warnings

bus = smbus.SMBus(1)
from gpiozero import LED
from time import sleep

led = LED(17)

#while True:
    #led.on()
    #sleep(1)
    #led.off()
    #sleep(1)

class PCA9685: #pour commander les sorties pwm
    def __init__(self, address_PCA9685=0x40):
        
        self.address_PCA9685 = address_PCA9685
        self.bus=bus
       
       # INITIALISATION / DÉFINITION des registres
        self.MODE1 = 0x00  # self.REGISTRE = adresse_registre
        self.MODE2 = 0x01

        self.LED0_ON_L = 0x06
        self.LED0_ON_H = 0x07
        self.LED0_OFF_L = 0x08
        self.LED0_OFF_H = 0x09

        self.LED1_ON_L = 0x0A
        self.LED1_ON_H = 0x0B
        self.LED1_OFF_L = 0x0C
        self.LED1_OFF_H = 0x0D

        self.LED2_ON_L = 0x0E
        self.LED2_ON_H = 0x0F
        self.LED2_OFF_L = 0x10
        self.LED2_OFF_H = 0x11

        self.LED3_ON_L = 0x12
        self.LED3_ON_H = 0x13
        self.LED3_OFF_L = 0x14
        self.LED3_OFF_H = 0x15

        self.PRE_SCALE = 0xFE


        # CONFIGURATION des registres du PCA9685 et initialisation des moteurs/variateurs
        # write_byte_data prend trois arguments: l'adresse de l'appareil i2C, le nom de registre où on veut écrire, les données à écrire (byte/octet en hexadécimal)
        bus.write_byte_data(self.address_PCA9685,self.MODE1,0x10)
        bus.write_byte_data(self.address_PCA9685,self.PRE_SCALE,64)
        bus.write_byte_data(self.address_PCA9685,self.MODE1,0x00)


        bus.write_byte_data(self.address_PCA9685,self.MODE2,0x04) 

        # Les quatre registres suivants permettent de définir précisément les intervalles d’allumage et d’extinction (largeur d'impulsion) pour chaque LED, ce qui permet de contrôler la position d’un moteur.
        # LED N°0
        bus.write_byte_data(self.address_PCA9685,self.LED0_ON_L,0)  
        bus.write_byte_data(self.address_PCA9685,self.LED0_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_L,0x40) #0x153 pour ancien variateur
        bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_H,1) #0x1 

        # LED N°1       
        bus.write_byte_data(self.address_PCA9685,self.LED1_ON_L,0) # 0x25 est la valeur hexadécimale de 37 : valeur médiane de 12 et 62 
        bus.write_byte_data(self.address_PCA9685,self.LED1_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_L,0x40) #0x153 pour ancien variateur
        bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_H,1) #0x1

        # LED N°2
        bus.write_byte_data(self.address_PCA9685,self.LED2_ON_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED2_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_L,153)
        bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_H,1)

        # LED N°3
        bus.write_byte_data(self.address_PCA9685,self.LED3_ON_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED3_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_L,153)
        bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_H,1)

        # PRE_SCALE (pour configurer la fréquence de la PWM (modulation de largeur d’impulsion) sur tous les canaux)
    def commande_moteur_vitesse_pourcentage(self,pourcent,num_moteur) :
        #valeur_milieu_periode=1227 # pour nouveau variateur
        valeur_milieu_periode=0x140      # pour ancien variateur
        temp_off_us=valeur_milieu_periode+pourcent*4.095  #valeur milieu de la commande => pour laquelle la vitesse est nulle
        temps_H = temp_off_us//256
        temps_L = temp_off_us%256
        
        #print("fonction ecrire_temps_off_us appel")
        if num_moteur == 0 :
            bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_L,int(temps_L))
            bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_H,int(temps_H))
        if num_moteur == 1 :
            bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_L,int(temps_L))
            bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_H,int(temps_H))
        if num_moteur == 2 :
            bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_L,int(temps_L))
            bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_H,int(temps_H))
        if num_moteur == 3 :
            bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_L,int(temps_L))
            bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_H,int(temps_H))
        if num_moteur == 4 :
            bus.write_byte_data(self.address_PCA9685,self.LED4_OFF_L,int(temps_L))
            bus.write_byte_data(self.address_PCA9685,self.LED4_OFF_H,int(temps_H))
        
class capteurs():

    def __init__(self, addresse_BNO055 = 0x28):
        self.address_BNO055 = addresse_BNO055 # centrale inertielle
        data = bus.read_i2c_block_data(self.address_BNO055,0x3F,1)
        data[0]=0x20
        bus.write_byte_data(self.address_BNO055,0x07,1)
        bus.write_byte_data(self.address_BNO055,0x08,0x08)
        bus.write_byte_data(self.address_BNO055,0x0A,0x23)
        bus.write_byte_data(self.address_BNO055,0x0B,0x00)
        bus.write_byte_data(self.address_BNO055,0x09,0x1B)
        bus.write_byte_data(self.address_BNO055,0x07,0)
        bus.write_byte_data(self.address_BNO055,0x40,0x01)
        bus.write_byte_data(self.address_BNO055,0x3B,0x01)
        bus.write_byte_data(self.address_BNO055,0x3E,0x00)
        bus.write_byte_data(self.address_BNO055,0x3D,0x0C)
        print("fin de l'initialisation")
        pass

class LidarTFLuna: # pour lire la distance mesurée par le LiDAR TF Luna en utilisant le protocole I2C
    def __init__(self, i2c_address=0x10, i2c_bus=1):
        # Initialiser le bus I2C
        self.address = i2c_address
        self.bus = smbus.SMBus(i2c_bus)
    
    def read_distance(self):
        # Le TF Luna envoie les données de distance en 2 octets
        try:
            # Lire les 2 bytes (octets) de données de distance
            distance_data = self.bus.read_i2c_block_data(self.address, 0x00, 2)  #arguments: adresse unique du périphérique, adresse du premier registre à lire,  nbre de bytes à lire
            # Combiner les 2 octets en une seule valeur de distance en cm
            distance = (distance_data[0] + (distance_data[1] << 8))
            return distance
        except Exception as e:
            print(f"Erreur de lecture du LiDAR TF Luna : {e}")
            return None
    
    
class brushless():
    def __init__(self):
        # J'initilise la vitesse des moteurs
        myPCA9685.commande_moteur_vitesse_pourcentage(0,0)
        myPCA9685.commande_moteur_vitesse_pourcentage(0,1)
    def commande(self, vitesse_pourcent, num_mot):
        myPCA9685.commande_moteur_vitesse_pourcentage(vitesse_pourcent,num_mot)
    
# Initialisation:
lidar = LidarTFLuna()
#capteur = capteurs()
alt_obj = 150
myPCA9685 = PCA9685()
mot_brushless=brushless()
print("Prêt - Initialisation réalisée")

# Boucle_continue/principale
while True : 
    # Télémètre infrarouge
    distance = lidar.read_distance()  
    print(f"La distance mesurée par le télémètre infrarouge est: {distance}cm")
    
    commande_vitesse_pourcentage=int(input("Donner la commande de vitesse du moteur en pourcentage (entre -100 et 100):"))
    numero_moteur=int(input("Donner numero moteur:"))
    #time.sleep(1)
    mot_brushless.commande(commande_vitesse_pourcentage,numero_moteur)
    
    #mot_brushless.commande(temps_off+50,numero_moteur)
    #time.sleep(2)
    #mot_brushless.commande(temps_off+100,numero_moteur)
    #time.sleep(2)
    #mot_brushless.commande(temps_off+150,numero_moteur)

    
    #distance_us, roll, pitch, yaw = capteur.get()
    # alt_mes = distance_us*np.cos(roll)*np.cos(pitch)*np.cos(yaw)
    # eps = alt_obj - alt_mes

