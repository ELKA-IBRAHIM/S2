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

#lorem(10)

= EXAM  2018
== Puissances actives et réactives
 + Puissance active 
 P = Re($underline(V).underline((I))$)
 + Puissance réactive
  Q = Im($underline(V).underline(I*)$)
 + Hypothèses pour passer du triphasé au monophasé.
  + Sys equilibré charges et tensions identiques.
  + Tensions sinusoïdales et déphasées de 120°.
  + Courant dans le neutre nul. 
  + Pas de couplage entre les phases. 
== Circuit magnétique 
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
