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
#   Projet
#
########################################################

import math as m
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import time
import os

########################################################
#Affichages
def affichage3D(Lcourbe):
    """
    Fonction d'affichage 3D \n
    On envoie les courbes que l'on veut afficher dans une liste.\n
    La liste contient un tuple qui correspond à une courbe.\n
    Ainsi chaque courbe est un tuple contenant les positions en X, Y et Z et le label de la courbe.\n
    """
    plt.figure()
    plt.subplot(projection='3d')
    plt.plot([0],[0],[0],'k+',markersize=10,label='Origine')
    for i in Lcourbe:
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
    axes.set_zlim((0,max(max(Lcourbe[0][2]),max(Lcourbe[1][2]))))
    plt.tight_layout()
    plt.legend()
    
def affichage2D(Lx,Lz,titre=''):
    """
    Fonction d'affichage 2D \n
    On envoie les positions horizontales, verticales dans des listes et la label de la courbe.
    """
    plt.figure()
    plt.subplot()
    plt.plot(Lx,Lz,'ro',label=titre)
    # plt.axis([Lx[0],Lx[-1], 0, 1000])
    plt.grid('--')
    plt.legend()
    plt.show()
    
    
    
    
########################################################
def Parametre(Lparametre):
    """
    Fonction contenant les paramètres nécessaire pour faire fonctionner la fonction canon.\n
    Variable d'entrée: liste des paramètres\n
    Les paramètres utiles seront des variables globales.
    """
    #Variable global
    global rho,S,Cx,Cy,Cz,g,vitesseInitiale,vitesseVent,masse,dt,alpha,theta,x0,y0,beta,t0
    x0=Lparametre[0]
    y0=Lparametre[1]
    theta=Lparametre[2]
    gamma=Lparametre[3]
    vitesseInitiale=Lparametre[4]
    masse=Lparametre[5]
    t0=Lparametre[6]
    
    alpha=theta*3.14/180
    beta=gamma*3.14/180
    
    vitesseVent=[0,0,0]
    
    rho=1.225
    S=(0.121/2)**2*np.pi
    Cx=0.3
    Cy=0.3
    Cz=0.3
    g=9.81
    dt=1e-1

    
    
def Canon(Lparametre):
    """
    Fonction qui calcule les positions en X, Y et Z du boulet de canon au cours du temps.\n
    Variable d'entrée: liste des paramètres\n
    Retourne des listes contenant les positions en X, Y et Z et la liste contenant les sensibilités pour chaque paramètres.\n
    On utilisera un algorithme d'Euler pour calculer les positions.\n
    On calculera aussi la sensibilité en fonction de chaque paramètre.
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
    
    #Définitions des conditions initiales
    Lt=[-t0]
    Ldx=[vitesseInitiale*np.cos(alpha)*np.cos(beta)]
    Ldy=[vitesseInitiale*np.cos(alpha)*np.sin(beta)]
    Ldz=[vitesseInitiale*np.sin(alpha)]
    Lx=[x0]
    Ly=[y0]
    Lz=[0]

    n0=int(10*t0)

    K=-0.5*rho*S*Cx #Constante pour le calcul de la sensibilité

    LS=[[[1],[0],[0],[0],[0],[0],[-Lx[-1]]],  #S de X
        [[0],[1],[0],[0],[0],[0],[-Ly[-1]]],  #S de Y
        [[0],[0],[0],[0],[0],[0],[-Lz[-1]]]]  #S de Z
    
    LdS=[[[0],[0],[-vitesseInitiale*np.sin(alpha)*np.cos(beta)],[-vitesseInitiale*np.cos(alpha)*np.sin(beta)],[np.cos(alpha)*np.cos(beta)],[0]],  
         [[0],[0],[-vitesseInitiale*np.sin(alpha)*np.sin(beta)],[vitesseInitiale*np.cos(alpha)*np.cos(beta)],[np.cos(alpha)*np.sin(beta)],[0]],    
         [[0],[0],[vitesseInitiale*np.cos(alpha)],[0],[np.sin(alpha)],[0]]]
  
    #Calcul des positions du canon au cours du temps avec Euler
    for i in range(n0+len(Lx0)-1):
        #Calcul des positions et vitesses à partir de la 1ère position mesuré
        Lt.append(Lt[-1]+dt)
        Ldx.append(Ldx[-1]+dt*fx(Ldx[-1]+vitesseVent[0]))
        Lx.append(Lx[-1]+dt*Ldx[-1])
        
        Ldy.append(Ldy[-1]+dt*fy(Ldy[-1]+vitesseVent[1]))
        Ly.append(Ly[-1]+dt*Ldy[-1])
        
        Ldz.append(Ldz[-1]+dt*(fz(Ldz[-1]+vitesseVent[2])-g))
        Lz.append(Lz[-1]+dt*Ldz[-1])
        
        #Calcul de la sensibilité
        LdS[0][0].append(2*K/masse*Ldx[-1]*LdS[0][0][-1]*dt+LdS[0][0][-1])#X x0
        LdS[0][1].append(2*K/masse*Ldx[-1]*LdS[0][1][-1]*dt+LdS[0][1][-1])#X y0        
        LdS[0][2].append(2*K/masse*Ldx[-1]*LdS[0][2][-1]*dt+LdS[0][2][-1])#X alpha
        LdS[0][3].append(2*K/masse*Ldx[-1]*LdS[0][3][-1]*dt+LdS[0][3][-1])#X beta
        LdS[0][4].append(2*K/masse*Ldx[-1]*LdS[0][4][-1]*dt+LdS[0][4][-1])#X V0
        LdS[0][5].append((-K*(Ldx[-1]**2)/(masse**2)+2*K/masse*LdS[0][5][-1]*Ldx[-1])*dt+LdS[0][5][-1])#X m
        LS[0][6].append(Lx[-1])#X t0

        LdS[1][0].append(2*K/masse*Ldy[-1]*LdS[1][0][-1]*dt+LdS[1][0][-1])#Y x0
        LdS[1][1].append(2*K/masse*Ldy[-1]*LdS[1][1][-1]*dt+LdS[1][1][-1])#Y y0        
        LdS[1][2].append(2*K/masse*Ldy[-1]*LdS[1][2][-1]*dt+LdS[1][2][-1])#Y alpha
        LdS[1][3].append(2*K/masse*Ldy[-1]*LdS[1][3][-1]*dt+LdS[1][3][-1])#Y beta
        LdS[1][4].append(2*K/masse*Ldy[-1]*LdS[1][4][-1]*dt+LdS[1][4][-1])#Y V0
        LdS[1][5].append((-K*(Ldy[-1]**2)/(masse**2)+2*K/masse*LdS[1][5][-1]*Ldy[-1])*dt+LdS[1][5][-1])#Y m
        LS[1][6].append(Ly[-1])#Y t0

        LdS[2][0].append(2*K/masse*Ldz[-1]*LdS[2][0][-1]*dt+LdS[2][0][-1])#Z x0
        LdS[2][1].append(2*K/masse*Ldz[-1]*LdS[2][1][-1]*dt+LdS[2][1][-1])#Z y0        
        LdS[2][2].append(2*K/masse*Ldz[-1]*LdS[2][2][-1]*dt+LdS[2][2][-1])#Z alpha
        LdS[2][3].append(2*K/masse*Ldz[-1]*LdS[2][3][-1]*dt+LdS[2][3][-1])#Z beta
        LdS[2][4].append(2*K/masse*Ldz[-1]*LdS[2][4][-1]*dt+LdS[2][4][-1])#Z V0
        LdS[2][5].append((-K*(Ldz[-1]**2)/(masse**2)+2*K/masse*LdS[2][5][-1]*Ldz[-1])*dt+LdS[2][5][-1])#Z m
        LS[2][6].append(Lz[-1])#Z t0

        for xyz in range(len(LdS)):
            for param in range(len(LdS[0])):
                LS[xyz][param].append(dt*LdS[xyz][param][-1]+LS[xyz][param][-1])   
                
    return(Lx,Ly,Lz,LS)

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
    return(-rho*S*Cy*dy**2/(2*masse))

def fz(dz):
    """
    Fonction de calcul de la force de frottement fluide selon Z \n
    Variable d'entrée: vitesse selon Z.\n
    Retourne la valeur de la force.
    """
    return(-rho*S*Cz*dz**2/(2*masse))
    
def Moindres_carres(Lparametre):
    """
    Fonction de calcul des moindres carrées entre les positions réelles et les positions calculés
    Variable d'entrée: liste des paramètres\n
    Retourne la valeur des moindres carrées et le gradient pour ce point.\n
    """
    Lx,Ly,Lz,LS=Canon(Lparametre)
    #Initialisation avec Ldi la liste des différences au carré selon l'axe i
    Ldx=[]
    Ldy=[]
    Ldz=[]
    t0=Lparametre[6]
    n0=int(10*t0)

    n=len(Lx0)

    Gradient=[0]*len(Lparametre)

    #Calcul des moindres carrées et du gradient sur tous les points de la courbe a retrouver
    for i in range(n):
        # print(len(Lx),i+n0,len(Lx0),i)
        if i+n0<len(Lx) and i<len(Lx0) and i+n0<len(LS[0][0]): #Sécurité
            #print(len(Lx),i+n0,len(Lx0),i,len(LS[0][0]))
            Ldx.append((Lx[i+n0]-Lx0[i])**2)
            Ldy.append((Ly[i+n0]-Ly0[i])**2)
            Ldz.append((Lz[i+n0]-Lz0[i])**2)
            #Calcul du gradient
            for j in range(len(Gradient)):
                Gradient[j]+=2*(Lx[i+n0]-Lx0[i])*LS[0][j][i+n0]
                Gradient[j]+=2*(Ly[i+n0]-Ly0[i])*LS[1][j][i+n0]
                Gradient[j]+=2*(Lz[i+n0]-Lz0[i])*LS[2][j][i+n0]
        else:
            print(len(Lx),i+n0,len(Lx0),i,len(LS[0][0]))
            
    MC=sum(Ldx+Ldy+Ldz)/len(Lx0)
    return MC,Gradient
    
    
def Descente_Gradient(p0=[0,0,45,45,10,10,0],FctAMinimiser=Moindres_carres,eps=1e-3): #Normal [0,0,45,45,10,10] Caesar [0,0,45,45,1000,50]
    """
    Fonction de descente de gradient avec les sensibilités
    Variable d'entrée: liste des paramètres initiales; la fonction utilisé pour minimiser, la valeur final maximale que l'on souhaite\n
    Retourne les paramètres finaux.\n
    """
    
    # Initialisation
    params = p0
    MC,gradient=FctAMinimiser(params) 
    print("Étape {:5d} : x0={:.3f}  y0={:.3f}  theta={:.3f}  gamma={:.3f}  V0={:.3f}  m={:.3f}  t0={:.1f} MC= {:.3e}".format(0,params[0],params[1],params[2],params[3],params[4],params[5],params[6],MC))
    LMC=[MC]
    
    # Boucle de descente de gradient
    n=0
    while MC>eps:
        n+=1
        # Mise à jour des paramètres de la descente de gradient
        #Pas adptatif
        gradient=normer(gradient)
        
        params_suivant=params[:]
        for i in range(len(params)):
            params_suivant[i]=params[i]-gradient[i]

        params_suivant[-3]=max(1,params_suivant[-3])
        params_suivant[-2]=max(1,params_suivant[-2])
        params_suivant[-1]=max(0,params_suivant[-1])

        MC,gradient_suivant=FctAMinimiser(params_suivant) 

        #limite en norme du gradient en fonction de la valeur de la fonction a minimiser
        normeMin=1e-2
        #Pas adaptatif dans la limite de la norme du gradient
        while MC>=LMC[-1] and np.linalg.norm(gradient)>=normeMin:
            for i in range(len(params)):
                gradient[i]*=0.5
                params_suivant[i]=params[i]-gradient[i]
            params_suivant[-3]=max(1,params_suivant[-3])
            params_suivant[-2]=max(1,params_suivant[-2])
            params_suivant[-1]=max(0,params_suivant[-1])
            MC,gradient_suivant=FctAMinimiser(params_suivant)
        
        #Mise à jour des paramètres
        params=params_suivant[:]
        gradient=gradient_suivant[:]
        LMC.append(MC)
        print("Étape {:5d} : x0={:.3f}  y0={:.3f}  theta={:.3f}  gamma={:.3f}  V0={:.3f}  m={:.3f}  t0={:.1f} MC= {:.3e}".format(n,params[0],params[1],params[2],params[3],params[4],params[5],params[6],MC))
        
        #Affichage 3D qui se met à jour toutes les 1000 étapes
        if n%100 == 0 :
            print('Refresh')
            L=Canon(params)
            plt.close()
            t0=params[-1]
            n0=int(10*t0)
            affichage3D([[L[0][n0:],L[1][n0:],L[2][n0:], 'courbe modélisée','r'],[Lx0,Ly0,Lz0,'courbe théorique','b'],[L[0][:n0+1],L[1][:n0+1],L[2][:n0+1], 'Début courbe modélisée','g--']])
            plt.draw()
            plt.savefig("Sensibilite "+str(n)+"iterations")
            plt.pause(0.1)
            
    # Affichage de l'étape finale   
    L=Canon(params)
    plt.close()
    n0=int(10*t0)
    affichage3D([[L[0][n0:],L[1][n0:],L[2][n0:], 'courbe modélisée','r'],[Lx0,Ly0,Lz0,'courbe théorique','b'],[L[0][:n0+1],L[1][:n0+1],L[2][:n0+1], 'Début courbe modélisée','g--']])
    plt.draw()
    print(">>> Fin: Étape {:5d} : x0={:.5f}  y0={:.5f}  theta={:.5f}  gamma={:.5f}  V0={:.5f}  m={:.5f} MC= {:.3e}".format(n,params[0],params[1],params[2],params[3],params[4],params[5],MC))
    fichier=open('Resultat.txt','a')
    fichier.write(FctAMinimiser.__name__+":\n Étape {:5d} : theta={:.5f}  V0={:.5f}  MC= {:.3e}\n".format(n,params[0],params[1],MC))
    fichier.close()
    return(params)   
    
def lecture_donnes(fichier='Donnees_test.txt'): 
    """
    Fonction de lecture des données de la courbe à retrouver
    Variable d'entrée: nom du fichier ou sont enregistré les données.\n
    Retourne les listes de positions selon X, Y et Z  \n
    """
    #lecture du fichier
    fichier=open(fichier,'r')
    doc=fichier.readlines()
    fichier.close()
    
    #Séparation des données et de l'entête (contient les paramètres exactes)
    lignes=doc[7:]
    entete=doc[:7]
    
    #Notation de l'entête dans un fichier ou l'on écrira les paramètres trouvés
    fichier2=open('Resultat.txt','a')
    fichier2.write('\n')
    fichier2.write('Canon 3D Sensibilités\n')
    for i in entete:
        fichier2.write(i)
    fichier2.write('\n')
    fichier2.close()
    
    #Création des listes de positions en global et d'une valeur contenant le nombre de positions 
    global Lx0,Ly0,Lz0,taille
    taille=len(lignes)
    Lx0=[]
    Ly0=[]
    Lz0=[]
    for ligne in lignes:
        position=(ligne.split('\n')[0]).split(';')
        Lx0.append(float(position[0]))
        Ly0.append(float(position[1]))
        Lz0.append(float(position[2]))

    return(Lx0,Ly0,Lz0)

def normer(L):
    """
    Fonction qui permet de normer une liste\n
    Variable d'entrée: liste \n
    Retourne la liste avec une norme de 10.\n
    """
    norme=np.linalg.norm(L)
    M=np.divide(L,norme/10)
    return(M)


from Creation_Donnes import FctCreation_Donnees

# FctCreation_Donnees()
FichierDonnees='Donnees_test.txt'
FctCreation_Donnees(FichierDonnees,type='V4')
tini=time.time()
lecture_donnes()
Descente_Gradient(FctAMinimiser=Moindres_carres,eps=1)
print('Temps de calcul: {:.5f} s'.format(time.time()-tini))
