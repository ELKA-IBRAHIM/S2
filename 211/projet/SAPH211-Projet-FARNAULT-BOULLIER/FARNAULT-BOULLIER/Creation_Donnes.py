# -*- coding: utf-8 -*-
########################################################
#
#   Auteur : Jules FARNAULT Paul BOULLIER (Mai Juin 2023)
#            Saphire, ENS Paris-Saclay
#
########################################################


########################################################
#
#   Saphire Module 211 Optimisation
#   Projet - Création des données
#
########################################################
import math as m
import numpy as np
import matplotlib.pyplot as plt
import random as rd
    
def Canon(Lparametre):
    global masse, rho,Cx,Cy,Cz,g,S
    #Paramètres étudiés
    x0=Lparametre[0]
    y0=Lparametre[1]
    theta=Lparametre[2]
    gamma=Lparametre[3]
    vitesseInitiale=Lparametre[4]
    masse=Lparametre[5]

    #Paramètres divers du système
    rho=1.225
    S=(0.121/2)**2*np.pi
    Cx=0.3
    Cy=0.3
    Cz=0.3
    g=9.81
    vitesseVent= [0,0,0] 
    dt=1e-1
    alpha=theta*3.14/180
    beta=gamma*3.14/180
    
    #Initialisation des listes
    Lt=[0]
    Ldx=[vitesseInitiale*np.cos(alpha)*np.cos(beta)]
    Ldy=[vitesseInitiale*np.cos(alpha)*np.sin(beta)]
    Ldz=[vitesseInitiale*np.sin(alpha)]
    Lx=[x0]
    Ly=[y0]
    Lz=[0]
    
    while Lz[-1]>=0 or len(Lt)==1:
        Lt.append(Lt[-1]+dt)
        Ldx.append(Ldx[-1]+dt*fx(Ldx[-1]+vitesseVent[0]))
        Lx.append(Lx[-1]+dt*Ldx[-1])
        
        Ldy.append(Ldy[-1]+dt*fy(Ldy[-1]+vitesseVent[1]))
        Ly.append(Ly[-1]+dt*Ldy[-1])
        
        Ldz.append(Ldz[-1]+dt*fz(Ldz[-1]+vitesseVent[2]))
        Lz.append(Lz[-1]+dt*Ldz[-1])
    return(Lx,Ly,Lz)



def fx(dx):
    return(-rho*S*Cx*dx**2/(2*masse))

def fy(dy):
    return(-rho*S*Cy*dy**2/(2*masse))

def fz(dz):
    return(-g-rho*S*Cz*dz**2/(2*masse))


def FctCreation_Donnees(nomFichier='Donnees_test.txt',type='V0'):
    

    if type=='V4':
        x=rd.randint(-10,10)
        y=rd.randint(-10,10)
        V=rd.randint(20,100)
        theta=rd.randint(5,85)
        gamma=rd.randint(0,180)
        m=rd.randint(1,10)
        

    elif type=='V2':
        x=rd.randint(-50,50)
        y=rd.randint(-50,50)
        V=rd.randint(5,100)
        theta=rd.randint(5,85)
        gamma=rd.randint(0,180)
        m=rd.randint(1,10)
        n0=0
    
    elif type=='V1':
        x=0
        y=0
        V=rd.randint(50,200)
        theta=rd.randint(5,85)
        gamma=0
        m=3
        n0=0

    else:
        assert False, 'Erreur création de données soit en version V1 (simple, 2 paramètres), V2(intermédiaire, 6 paramètres) ou V4 (complexe, 7 paramètres)'

    params=[x,y,theta,gamma,V,m]
    Lx,Ly,Lz=Canon(params)

    if type=='V4':
        n0=int(len(Lx)*(rd.uniform(0.1, 0.5)))
        
    print('x0= '+str(x)+' \n'+'y0= '+str(y)+' \n'+'theta= '+str(theta)+' \n'+'gamma= '+str(gamma)+' \n'+'V0= '+str(V)+' \n'+'m= '+str(m)+' \n'+'t0='+str(n0/10)+' \n')
    
    fichier=open(nomFichier,'w')
    fichier.write('x0= '+str(x)+' \n')
    fichier.write('y0= '+str(y)+' \n')
    fichier.write('theta= '+str(theta)+' \n')
    fichier.write('gamma= '+str(gamma)+' \n')
    fichier.write('V0= '+str(V)+' \n')
    fichier.write('m= '+str(masse)+' \n')
    fichier.write('t0='+str(n0/10)+' \n')

    for i in range(n0,len(Lx)):
        fichier.write(str(Lx[i])+';'+str(Ly[i])+';'+str(Lz[i])+'\n')

    fichier.close()
    print('Document Fait \n')








