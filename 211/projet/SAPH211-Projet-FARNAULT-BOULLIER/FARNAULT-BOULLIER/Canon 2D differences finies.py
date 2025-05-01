# -*- coding: utf-8 -*-
########################################################
#
#   Auteur : Jules FARNAULT Paul BOULLIER (Janvier 2023)
#            Saphire, ENS Paris-Saclay
#
########################################################


########################################################
#
#   Saphire Module 211 Optimisation
#   Projet
#
########################################################

import math as m
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import time


from mpl_toolkits.mplot3d import axes3d  # Fonction pour la 3D
########################################################
    
def affichage2D(L):
    """
    Fonction d'affichage 2D \n
    On envoie les positions horizontales, verticales dans des listes et le label de la courbe.
    """
    for i in L:
        plt.plot(i[0],i[1],label=i[2])
        plt.grid('--')
        plt.legend()
    
########################################################    
    
def Canon(Lparametre):
    """
    Fonction qui calcule les positions en X, Y et Z du boulet de canon au cours du temps.\n
    Variable d'entrée: liste des paramètres\n
    Retourne des listes contenant les positions en X, Y et Z.\n
    On utilisera un algorithme d'Euler pour calculer les positions.
    """
    global rho,S,Cx,g,vitesseInitiale,vitesseVent,masse,dt,alpha,theta
    theta=Lparametre[0]
    vitesseInitiale=Lparametre[1]

    #Passage des angles de deg en rad
    alpha=theta*3.14/180

    #Autres paramètres divers
    vitesseVent=[0,0,0]
    rho=1.225
    S=(0.121/2)**2*np.pi
    Cx=0.3
    g=9.81
    masse=3
    dt=1e-1

    #Initialisation des listes des postions, vitesses et du temps
    Lt=[0]
    Ldx=[vitesseInitiale*np.cos(alpha)]
    Ldy=[0]
    Ldz=[vitesseInitiale*np.sin(alpha)]
    Lx=[0]
    Ly=[0]
    Lz=[0]
    
    #Calcul par récursivité des vitesses et positions
    while len(Lt)<len(Lx0):
        Lt.append(Lt[-1]+dt)
        Ldx.append(Ldx[-1]+dt*fx(Ldx[-1]+vitesseVent[0]))
        Lx.append(Lx[-1]+dt*Ldx[-1])
        
        Ldy.append(Ldy[-1]+dt*fy(Ldy[-1]+vitesseVent[1]))
        Ly.append(Ly[-1]+dt*Ldy[-1])
        
        Ldz.append(Ldz[-1]+dt*fz(Ldz[-1]+vitesseVent[2]))
        Lz.append(Lz[-1]+dt*Ldz[-1])
    return(Lx,Ly,Lz)

def fx(dx):
    """
    Fonction de calcul de la force de frottement fluide selon X\n
    Variable d'entrée: vitesse selon X.\n
    Retourne la valeur de la force.
    """
    return(-rho*S*Cx*dx**2/(2*masse))

def fy(dy):
    """
    Fonction de calcul de la force de frottement fluide selon Y\n
    Variable d'entrée: vitesse selon Y.\n
    Retourne la valeur de la force.
    """
    return(-rho*S*Cx*dy**2/(2*masse))

def fz(dz):
    """
    Fonction de calcul de la force de frottement fluide selon Z \n
    Variable d'entrée: vitesse selon Z.\n
    Retourne la valeur de la force.
    """
    return(-g-rho*S*Cx*dz**2/(2*masse))

    
def Moindres_carres(Lparametre):
    """
    Fonction de calcul des moindres carrées entre les positions réelles et les positions calculés
    Variable d'entrée: liste des paramètres\n
    Retourne la valeur des moindres carrées pour ce tuple de paramètres.\n
    """
    Lx,Ly,Lz=Canon(Lparametre)
    #Initialisation Ldi: listes des différences aux carrées de chaque point selon l'axe i
    Ldx=[]
    Ldy=[]
    Ldz=[]
    
    #Calcul des moindres carrés
    for i in range(len(Lx0)):
        Ldx.append((Lx[i]-Lx0[i])**2)
        Ldy.append((Ly[i]-Ly0[i])**2)
        Ldz.append((Lz[i]-Lz0[i])**2)
    MC=sum(Ldx+Ldy+Ldz)/len(Lx0)
    return MC
    
    
def Descente_Gradient(p0=[45,10],FctAMinimiser=Moindres_carres,eps=1e-3):
    """
    Fonction de descente de gradient par différences finies
    Variable d'entrée: liste des paramètres initiales; la fonction utilisé pour minimiser, la valeur final maximale que l'on souhaite\n
    Retourne les paramètres finaux.\n
    """

    # Initialisation
    delta = 1e-6
    params = p0
    MC=FctAMinimiser(params) 
    print("Étape {:5d} : theta={:.3f}  V0={:.3f}  MC= {:.3e}".format(0,params[0],params[1],MC))
    LMC=[MC]
    
    # Boucle de descente de gradient
    n=0
    while MC>eps:
        n+=1 
        # Calcul du gradient estimé de la fonction de perte au point actuel
        gradient = [0]*len(params)
        
        for j in range(len(params)):
            params_plus = np.copy(params)
            params_plus[j] += delta
            params_moins = np.copy(params)
            params_moins[j] -= delta
            gradient[j] = (FctAMinimiser(params_plus) - FctAMinimiser(params_moins)) / (2*delta)
        
        #Pas adptatif
        gradient=normer(gradient)
        params_suivant=[]
        for i in range(len(params)):
            params_suivant.append(params[i]-gradient[i])

        #Sécurité
        params_suivant[-1]=max(1,params_suivant[-1])

        MC=FctAMinimiser(params_suivant) 

        #limite en norme du gradient en fonction de la valeur de la fonction a minimiser
        normeMin=1e-4
        #Pas adaptatif dans la limite de la norme du gradient
        while MC>LMC[-1] and np.linalg.norm(gradient)>=normeMin:
            for i in range(len(params)):
                gradient[i]*=0.5
                params_suivant[i]=params[i]-gradient[i]
            #Sécurité
            params_suivant[-1]=max(1,params_suivant[-1])    
            MC=FctAMinimiser(params_suivant)

        #Mise à jour des paramètres et affichage des résultats
        params=params_suivant[:]
        
        LMC.append(MC)
        print("Étape {:5d} : theta={:.3f}  V0={:.3f}  MC= {:.3e}".format(n,params[0],params[1],MC))
    
        #Affichage 3D qui se met à jour toutes les 100 étapes
        if n%10==0 :
            # Affichage de l'étape finale   
            Lx,Ly,Lz=Canon(params)
    
            plt.close()
            affichage2D([[Lx0,Lz0,'Canon théorique'],[Lx,Lz,'Canon trouvé']])
            plt.draw()
            plt.savefig("2D "+str(n)+"iterations")
            plt.pause(0.5)
            
    # Affichage de l'étape finale   
    print(">>> Fin: Étape {:5d} : theta={:.3f}  V0={:.3f}  MC= {:.3e}".format(n,params[0],params[1],MC))
    Lx,Ly,Lz=Canon(params)

    plt.close()
    affichage2D([[Lx0,Lz0,'Canon théorique'],[Lx,Lz,'Canon trouvé']])
    plt.draw()
    plt.pause(2)
    plt.savefig("2D "+str(n)+"iterations")
    plt.close()
    affichage2D([[[i for i in range(len(LMC))], LMC,'Moindres carrées']])
    plt.draw()
    plt.pause(2)
    plt.savefig("2D MC au cours des itérations")
    
    #Enregistrement du résultat dans un fichier
    fichier=open('Resultat.txt','a')
    fichier.write(FctAMinimiser.__name__+":\n Étape {:5d} : theta={:.5f}  V0={:.5f}  MC= {:.3e}\n".format(n,params[0],params[1],MC))
    fichier.close()
        
    return(params)

def lecture_donnes(Donnees='Donnees_test.txt',Sortie='Resultat.txt'): 
    """
    Fonction de lecture des données de la courbe à retrouver
    Variable d'entrée: nom du fichier ou sont enregistré les données et nom du fichier ou l'on enregistre les résultats.\n
    Retourne les listes de positions selon X, Y et Z  \n
    """
    #lecture du fichier de données
    fichier=open(Donnees,'r')
    doc=fichier.readlines()
    fichier.close()
    
    #Séparation des données et de l'entête (contient les paramètres exactes)
    lignes=doc[7:]
    autre=doc[:7]
    
    # #Notation de l'entête dans un fichier ou l'on écrira les paramètres trouvés
    fichier2=open(Sortie,'a')
    fichier2.write('\n')
    fichier2.write('Canon 2D différences finies\n')
    for i in autre:
        fichier2.write(i)
    fichier2.write('\n')
    fichier2.close()

    #Création des listes de positions en global et d'une valeur contenant le nombre de positions 
    global Lx0,Ly0,Lz0,taille
    taille=len(lignes)
    Lx0=[]
    Ly0=[]
    Lz0=[]
    for i in range(taille):
        ligne=lignes[i].split('\n')[0]
        k=ligne.split(';')
        Lx0.append(float(k[0]))
        Ly0.append(float(k[1]))
        Lz0.append(float(k[2]))
    return(Lx0,Ly0,Lz0)

def normer(L):
    """
    Fonction qui permet de normer (avec un coefficient 10) une liste\n
    Variable d'entrée: liste \n
    Retourne la liste avec une norme de 1.\n
    """
    norme=np.linalg.norm(L)
    M=np.divide(L,norme)
    return(M)


from Creation_Donnes import FctCreation_Donnees

FichierSortie='Resultat.txt'
FichierDonnees='Donnees_test.txt'
FctCreation_Donnees(FichierDonnees,type='V1')
tini=time.time()
lecture_donnes(FichierDonnees,FichierSortie)
Descente_Gradient(FctAMinimiser=Moindres_carres,eps=1e-5)
print('Temps de calcul: {:.5f} s'.format(time.time()-tini))
    

