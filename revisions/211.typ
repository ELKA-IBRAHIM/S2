#import "@preview/callisto:0.1.0"


#set text(font: "New Computer Modern")
// #show raw: set text(font: "New Computer Modern Mono")
// Début Title Page
// 
//

#set align(center)
#align(center, text(17pt)[
  *Révivsion pour l'exam de 211*
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

#lorem(10)

= EXAM  2017/2018
== Régression polynomiale
 - Classique 
== Estimation ensembliste
- Justification de l'estimé 
  - Bruit borné donc y($theta$,k) borné  
- Ensemble vide 
  - si les bornes sur les bruits sont trop petites
  - si le modèle est inadapté
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
