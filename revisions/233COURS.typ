#import "@preview/callisto:0.1.0"


#set text(font: "New Computer Modern")
// #show raw: set text(font: "New Computer Modern Mono")
// Début Title Page
// 
//

#set align(center)
#align(center, text(17pt)[
  *Révivsion pour l'exam de 233*
])
*Ibrahim EL KASSIMI*   
#grid(
  align(center)[
    Ibrahim El Kassimi \
     École Normale Supérieure Paris-Saclay \
     #link("mailto:ibrahim.el_kassimi@ens-paris-saclay.fr")
  ]
)
#align(center)[
  #set par(justify: false)
    *Abstract* \
    Ce document contient les remarques et les formules importantes prises lors de la révision pour l'examen de 233.\
]
#set align(left)
#set heading(numbering: "1.")
#counter(heading).update(0)
// Fin Title Page


#outline()
#pagebreak()

= Elec num
// Chapitre 1
== #rect("Les Hacheurs" , fill: gradient.linear(..color.map.spectral))
- ELaborer la commande des structures 
  - Créer des dents de scie 
  - comparateur entre (le dents de scie et un signal constant)
- fct de modulation (= 0 ou 1)
- Transfert direct ou indirect 
  - Indirect : Présence d'élement de stickage entre la source de tension et la source de courant.
- Natures des interrupteurs
  - caractérisriques des interrupteurs.   
  - Attention!! convention passif 
- Polarisation de la diode.
- Grandeurs d'état:
  - La tension aux bornes du condensateur. 
  - Le courant traversant la bobine.
- Valeurs moyennes nulles 
  - <$v_l$> = 0
  - <$i_c$> = 0
- Calcul de la valeur moyenne 
  - souvent avec des aires sous les courbes.
#figure(image("figures/PolarisationDiode.png", width: 50%),
    caption: [Polarisation  diode])<polarisation>
+ Puissance active 
P = Re($underline(V).underline((I))$)
+ Puissance réactive
Q = Im($underline(V).underline(I*)$)
+ Hypothèses pour passer du triphasé au monophasé.
+ Sys equilibré charges et tensions identiques.
+ Tensions sinusoïdales et déphasées de 120°.
+ Courant dans le neutre nul. 
+ Pas de couplage entre les phases. 
// Chapitre 2
== #rect("Conversion DC-DC isolée", fill:gradient.linear(..color.map.spectral))
- Interêts de l'isolation 
  - Séccurité.
  - Adaptation de la tension.
  - Adaptation de l'impédance.
- 3 RELATIONS inductance mutuelle
  - //$:= cases(1 $sum_i n i = frak(R) phi$)$
  - $  cases(
  sum_i n i = frak(R) phi space [R = 0 "Pour un transfo"] ,
  v_1 = n_1 frac(d phi, d t),
  v_2 = n_2 frac(d phi, d t),
) $
- B = $mu_0 mu_r H$
- Thé d'Ampère $integral_v (arrow("H")arrow("dl")) = sum("I_enlacés")$
- $W_"mag" = integral_v arrow(H)arrow(B)"dv"$
  - $W_"entrefer" >> W_"fer"$ 
- mu_0 = $4pi 10^(-7)$
- $R = frac(l,mu S)$
- N$phi=L I$ et N$I = frak(R)_"tot" phi$ ($frak(R)_"tot"$: la reluctrance totale du C.M)
donc $N^2 I = frak(R)_"tot" Phi$ \
d'ou $L = frac(Phi,I) = frac(N^2,frak(R)_"tot")$ #rect($L= frac(N^2,frak(R)_"tot")$)
- 
== Machine électrique élemenatire

  
= Conclusion
