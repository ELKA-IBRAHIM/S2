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

########################################################
#Affichages
def affichage3D(L):
    """
    Fonction d'affichage 3D \n
    On envoie les courbes que l'on veut afficher dans une liste.\n
    La liste contient un tuple qui correspond à une courbe.\n
    Ainsi chaque courbe est un tuple contenant les positions en X, Y et Z, le label de la courbe et sa couleur.\n
    """
    plt.figure()
    plt.subplot(projection='3d')
    plt.plot([0],[0],[0],'k+',markersize=10,label='Origine')
    for i in L:
    # Tracé du résultat en 3D
        plt.subplot(projection='3d')
        plt.plot(i[0],i[1],i[2],i[4],label=i[3])
        if len(i[0])>0:
            plt.plot(i[0][0],i[1][0],i[2][0],i[4][0]+'+',markersize=10)
    #Ajustement des axes
    axes = plt.gca()
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    axes.set_zlabel('z')
    axes.set_zlim((0,max(max(L[0][2]),max(L[1][2]))))
    plt.tight_layout()
    plt.legend()
    
def affichage2D(Lx,Lz,titre=''):
    """
    Fonction d'affichage 2D \n
    On envoie les positions horizontales, verticales dans des listes et le label de la courbe.
    """
    plt.figure()
    plt.subplot()
    plt.plot(Lx,Lz,'ro',label=titre)
    plt.grid('--')
    plt.legend()
    plt.show()
    
    
    
def Canon(Lparametre):
    """
    Fonction qui calcule les positions en X, Y et Z du boulet de canon au cours du temps.\n
    Variable d'entrée: liste des paramètres\n
    Retourne des listes contenant les positions en X, Y et Z.\n
    On utilisera un algorithme d'Euler pour calculer les positions.
    """
    global rho,S,Cx,Cy,Cz,g,masse

    x0=Lparametre[0]
    y0=Lparametre[1]
    theta=Lparametre[2]
    gamma=Lparametre[3]
    vitesseInitiale=Lparametre[4]
    masse=Lparametre[5]
    t0=Lparametre[6]
    
    #Passage des angles de deg en rad
    alpha=theta*3.14/180
    beta=gamma*3.14/180
    
    #Autres paramètres divers
    vitesseVent=[0,0,0]
    rho=1.225
    S=(0.121/2)**2*np.pi
    Cx=0.3
    Cy=0.3
    Cz=0.3
    g=9.81
    dt=1e-1
    
    #Initialisation des listes des postions, vitesses et du temps
    Lt=[-t0]
    Ldx=[vitesseInitiale*np.cos(alpha)*np.cos(beta)]
    Ldy=[vitesseInitiale*np.cos(alpha)*np.sin(beta)]
    Ldz=[vitesseInitiale*np.sin(alpha)]
    Lx=[x0]
    Ly=[y0]
    Lz=[0]
    n0=max(int(10*t0),0)

    #Calcul par récursivité des vitesses et positions
    while len(Lt)-n0<len(Lx0):
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
    Retourne la valeur des moindres carrées ce point.\n
    """
    Lx,Ly,Lz=Canon(Lparametre)
    #Initialisation Ldi: listes des différences aux carrées de chaque point selon l'axe i
    Ldx=[]
    Ldy=[]
    Ldz=[]
    t0=Lparametre[6]
    n0=max(int(10*t0),0)
    n=len(Lx0)
    
    #Calcul des moindres carrés
    for i in range(0,n):
        if i+n0<len(Lx) and i<len(Lx0): #Sécurité
            Ldx.append((Lx[i+n0]-Lx0[i])**2)
            Ldy.append((Ly[i+n0]-Ly0[i])**2)
            Ldz.append((Lz[i+n0]-Lz0[i])**2)
        else:
            print(len(Lx),i+n0,len(Lx0),i)
            
    MC=sum(Ldx+Ldy+Ldz)/len(Lx0)
    return MC
    
    
def Descente_Gradient(p0=[0,0,45,45,10,10,0],FctAMinimiser=Moindres_carres,eps=1e-3): #Normal [0,0,45,45,10,10] Caesar [0,0,45,45,1000,50]
    """
    Fonction de descente de gradient par différences finies
    Variable d'entrée: liste des paramètres initiales; la fonction utilisé pour minimiser, la valeur final maximale que l'on souhaite\n
    Retourne les paramètres finaux.\n
    """

    # Initialisation
    delta = 1e-6
    params = p0
    MC=FctAMinimiser(params) 
    print("Étape {:5d} : x0={:.3f}  y0={:.3f}  theta={:.3f}  gamma={:.3f}  V0={:.3f}  m={:.3f}  t0={:.1f} MC= {:.3e}".format(0,params[0],params[1],params[2],params[3],params[4],params[5],params[6],MC))
    LMC=[MC]
    
    # Boucle de descente de gradient
    n=0
    while MC>eps:
        n+=1          
        # Calcul du gradient estimé de la fonction de perte au point actuel
        gradient = [0]*len(params)
        
        for j in range(len(params)-1):
            params_plus = np.copy(params)
            params_plus[j] += delta
            params_moins = np.copy(params)
            params_moins[j] -= delta
            gradient[j] = (FctAMinimiser(params_plus) - FctAMinimiser(params_moins)) / (2*delta)

        #Gestion a part du paramètre t0 car il faut un pas de 0.1 pour avoir de l'effet
        params_plus = np.copy(params)
        params_plus[-1] += 1e-1
        params_moins = np.copy(params)
        params_moins[-1] -= 1e-1
        gradient[-1] = (FctAMinimiser(params_plus) - FctAMinimiser(params_moins)) / (2*1e-1)
            
        # Mise à jour des paramètres de la descente de gradient
        gradient=normer(gradient)
        params_suivant=params[:]
        for i in range(len(params)):
            params_suivant[i]=params[i]-gradient[i]

        #Sécurité
        params_suivant[-3]=max(1,params_suivant[-3])
        params_suivant[-2]=max(1,params_suivant[-2])
        params_suivant[-1]=max(0,params_suivant[-1])

        MC=FctAMinimiser(params_suivant) 

        #limite en norme du gradient en fonction de la valeur de la fonction a minimiser
        normeMin=1e-2
        #Pas adaptatif dans la limite de la norme du gradient
        while MC>LMC[-1] and np.linalg.norm(gradient)>=normeMin:
            for i in range(len(params)):
                gradient[i]*=0.5
                params_suivant[i]=params[i]-gradient[i]
            #Sécurité
            params_suivant[-3]=max(1,params_suivant[-3])
            params_suivant[-2]=max(1,params_suivant[-2])
            params_suivant[-1]=max(0,params_suivant[-1])    
            MC=FctAMinimiser(params_suivant)
        
        #Mise à jour des paramètres et affichage des résultats
        params=params_suivant[:]
        LMC.append(MC)
        print("Étape {:5d} : {} mesures  x0={:.3f}  y0={:.3f}  theta={:.3f}  gamma={:.3f}  V0={:.3f}  m={:.3f}  t0={:.1f} MC= {:.3e}".format(n,nbdemesure,params[0],params[1],params[2],params[3],params[4],params[5],params[6],MC))

        #on actualise les positions du projectile
        lecture_donnes(FichierDonnees,FichierSortie,etat=False)

        #Affichage 3D qui se met à jour toutes les 100 étapes
        if n%100 == 0 :
            L=Canon(params)
            plt.close()
            t0=params[6]
            n0=int(10*t0)
            affichage3D([[L[0][n0:],L[1][n0:],L[2][n0:], 'courbe modélisée','r'],[Lx0,Ly0,Lz0,'courbe théorique','b'],[L[0][:n0+1],L[1][:n0+1],L[2][:n0+1], 'Début courbe modélisée','g--']])
            plt.draw()
            plt.savefig("Recursivite "+str(n)+"iterations")
            plt.pause(0.1)
            
    # Affichage de l'étape finale   
    L=Canon(params)
    plt.close()
    t0=params[6]
    n0=int(10*t0)
    affichage3D([[L[0][n0:],L[1][n0:],L[2][n0:], 'courbe modélisée','r'],[Lx0,Ly0,Lz0,'courbe théorique','b'],[L[0][:n0+1],L[1][:n0+1],L[2][:n0+1], 'Début courbe modélisée','g--']])
    plt.draw()
    print(">>> Fin: Étape {:5d} : x0={:.5f}  y0={:.5f}  theta={:.5f}  gamma={:.5f}  V0={:.5f}  m={:.5f} MC= {:.3e}".format(n,params[0],params[1],params[2],params[3],params[4],params[5],MC))
    
    #Enregistrement du résultat dans un fichier
    fichier=open('Resultat.txt','a')
    fichier.write(FctAMinimiser.__name__+":\n Étape {:5d} : theta={:.5f}  V0={:.5f}  MC= {:.3e}\n".format(n,params[0],params[1],MC))
    fichier.close()

    return(params)   
    
def lecture_donnes(Donnees='Donnees_test.txt',Sortie='Resultat.txt',etat=True): 
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
    if etat:
        fichier2=open(Sortie,'a')
        fichier2.write('\n')
        fichier2.write('Canon 3D Récusivité\n')
        for i in autre:
            fichier2.write(i)
        fichier2.write('\n')
        fichier2.close()

    #Création des listes de positions en global et d'une valeur contenant le nombre de positions 
    global Lx0,Ly0,Lz0,taille,nbdemesure
    taille=len(lignes)
    Lx0=[]
    Ly0=[]
    Lz0=[]
    deltaTemps=time.time()-tini
    nbdemesure=min(int(deltaTemps*10)+5,taille)
    for i in range(nbdemesure):
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
    M=np.divide(L,norme/50)
    return(M)


from Creation_Donnes import FctCreation_Donnees

global FichierSortie,FichierDonnees
FichierSortie='Resultat.txt'
FichierDonnees='Donnees_test.txt'
FctCreation_Donnees(FichierDonnees,type='V4')
global nbdemesure
nbdemesure=0
tini=time.time()
lecture_donnes(FichierDonnees,FichierSortie)
Descente_Gradient(FctAMinimiser=Moindres_carres,eps=1)
print('Temps de calcul: {:.5f} s'.format(time.time()-tini))