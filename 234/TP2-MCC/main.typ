#import "@preview/callisto:0.1.0"
#import "@preview/datify:0.1.3": custom-date-format
#import "@preview/ctheorems:1.1.3": *
#import "@preview/mannot:0.3.0"

///// Les blocs contextuels /////
// bloc définition (style mathématique)
#let def = thmbox("definition", "Definition", inset: (x: 1.2em, top: 1em))

// bloc proposition (style mathématique)
#let prop = thmbox("proposition", "Proposition", inset: (x: 1.2em, top: 1em)).with(numbering: none)

// bloc de preuve/démonstration (style mathématique)
#let proof = thmproof("proof", "Preuve")

// bloc de remarque
#let remarque(contenu) = block(
  fill: rgb(230, 240, 255),
  radius: 4pt,
  inset: 8pt,
  width: 100%,
  text(fill: blue, size: 0.9em, smallcaps("Remarque") + ": "+
  contenu
  )
)

#let space = h(0.25em)

#let warning(body, icon: "⚠️") = block(
  fill: rgb(255, 244, 229),  // Fond jaune très clair
  inset: 1em,
  radius: 0.5em,
  width: 100%,
  stroke: (
    left: 4pt + rgb(255, 196, 9),  // Bordure gauche épaisse
    top: 0.5pt + rgb(255, 196, 9),
    bottom: 0.5pt + rgb(255, 196, 9),
    right: 0.5pt + rgb(255, 196, 9)
  ),
  text(rgb(179, 98, 0),strong(icon)+" "+body)
)

// bloc pour encadrer des résultats
#let result(text)=mannot.markrect(
    text,
    color: red,
    radius: 1pt,
    outset: 4pt
  )

// numérotation des équations
#set math.equation(numbering: "[1]")

// police de caractère
#set text(font: "New Computer Modern", lang:"fr")

// pour les numéros de page
#let in-outline = state("in-outline", false)
#set page(
  paper: "a4",
  numbering: (..n) => context {
    if in-outline.get() {
      str(n.at(0))
    } else {
      "- " + str(n.at(0)) + " -" 
    }
  }
)
#show outline: it => {
  in-outline.update(true)
  it
  in-outline.update(false)
}

///// Début Title Page /////
#set align(center)
#grid(
  columns: (1fr, 1fr),
  gutter: 0pt,
  // Left image (30% width, auto height)
  image("logo.png", width: 50%),
  // Right image (30% width, vertically centered with left)
  align(center + horizon)[
    #image("logo_upsaclay.jpg", width: 60%)
  ]
)

// pour la date
#custom-date-format(datetime.today(), "DD month YYYY", "fr")

#align(center, text(17pt)[
  *TP - 234 - Commande en régulation de vitesse d'une machine à courant continu*
])

    *Ibrahim El Kassimi*
    // École Normale Supérieure Paris-Saclay \
    // #link("mailto:ibrahim.elkassimi@ens-paris-saclay.fr")
\
*Encadrement par Cécile Durieu* \

// pour la numérotation des sections
#set align(left)
#set heading(numbering: "1.")
#counter(heading).update(0)

// pour la table des matières
#outline()

///// Fin Title Page /////

#pagebreak()

#let s = $omega_c$

= Préparation 1
== Détermination de  $G_0$ et $tau$ à partir de la réponse indicielle du système petits signaux en boucle ouverte.

=== Identification temporelle.

\
On a#space #result[$V(tau)=0,63(V_"final"-V_"initial"))+V_"initial"$]

Donc on en déduit  $tau$ .

De plus,#space #result[$G_0 = (V(#s)_"final"-V(#s)_"initial")/(U_"final"-U_"initial")$]

Par lecture graphique, on obtient #space#result[$tau=50$ ms et $G_0=1,2$]

=== Identification harmonique

\
En harmonique, on a #space #result[$phi(omega=1/tau)=-frac(pi,4)$]#space#space, on en déduit $tau$.

De plus#space #result[$G(omega=0)=G_0$]#space#space.


= Manipulation 1

== Détermination de   $Omega_0$

Pour une tension d'entrée $U_0=5$ V, on obtient
$V(Omega_0)=5,5$ V. Donc $Omega_0=5,5$ rad/s.

== Méthode pour soustraire $Omega_0$

Pour avoir un  fonctionnement en petits signaux, il faut soustraire précisément $Omega_0$ à $omega_c (t)$.
On envoie une tension continue $U_0$ au système et on moyenne la tension $V-E$ de sortie avec un multimètre. Enfin, on adapte le potentiomètre de $E$ jusqu'à avoir une moyenne de $#s$ nulle pour $u(t)=0$

= Identification
// Figure manip1_reponse_indicielle_syst.png
figure

#figure(
  image("figures2/Manip1.png", width: 100%),
  caption: [Réponse indicielle],
) <fig-manip1_reponse_indicielle_syst>


*Remarque*
Le phénomène vu à la fin du cycle peut être exliqué par le choc entre les dents au niveau de l'accouplement moteur réducteur.
 - $V(#s)_"final"-V(#s)_"initial"=7,28$ V

 - $V(#s)_"0,63%"=0,63(V_"final"-V_"initial")+V_"initial"=1,8$ V
 - $tau = 56,19$ ms
 - $G_0=1,21"rad" dot s^(-1) dot V^(-1)$
 - $frac(Omega_0,U_0)=1,1$
La différence entre $G_0$ et $frac(Omega_0,U_0)$ est due à la non linéarité introduite par les frottement secs.

== Étude en régime harmonique 
Pour faire l'étude harmoique on envoie plusieurs entrées sinusoïdales de fréquences différentes et on établit le diagramme de Bode du système.
On risque que, pour les hautes fréquences, l'influnce du bruit sur les mesure sera importante.

= Préparation 2
== Choix de la pulsation de coupure du filtre.
Pourquoi ne pas prendre une pulsation de coupure du filtre plus basse afin d'éliminer plus de bruit ?
Il faut éviter que le filtre impacte la dynamique du système dans la bande passante de la MCC.

== Choix de la valeur du facteur d'amortissement $xi$ 

Pour éviter les résonnances on prend #space #result[$xi>=1/sqrt(2)$]

*Comment s'assurer que  le filtre a été "correctement" ?*

On peut vérifier que l'écart entre les deux signaux  est uniquement du aux bruits de mesure.

= Manipulation 2
== Comparaison entre le signal filtré et non-filtré
// figure manip2_comparaison_filtre

 Pour assurer d'éviter les résonnances, on prend $xi=0,8$. On adapte la fréquence de coupure du filtre, plus elle est basse, plus le signal est filtré, mais plus le signal est distordu. On prend un compromis à $f=56,65 $ Hz.

#figure(
  image("figures2/avant_apres_filtre.png", width: 100%),
  caption: [réponse indicielle ],
) <fig-manip2_comparaison_filtre>


On observe que le filtre induit un retard  au début de chaque transition mais le temps de réponse est pratiquement le même, On conserve bien le comportement global du sysyème.



 - $V_"0,63%"=0,63(V_"final"-V_"initial")+V_"initial"=0,84$ V
 - $tau=56,24$ ms
 - $G_0=1,20 "rad" dot s^(-1) dot V^(-1)$


= Préparation 3
Par superposition on peut montrer que les deux schémas sont équivalents avec #space #result[$cases(U(t)=U_0+u(t), omega_c (t)=Omega_0+#s (t))$]

= Préparation 4
== Correction proportionnel
\
 - #result[$T_"BF" (p)=(K G_0)/(1+K G_0) 1/(1+tau/(1+K G_0) p)$]
\
 - #result[$t_(r,5%) = (3tau)/(1+K G_0)$]
\
 - #result[Gain statique $= (K G_0)/(1+K G_0)$]
\
Pour avoir un temps de réponse à 5% du système en BF 3 fois plus petit on prends #space#result[$K_1=2/G_0$]#space#space.

= Manipulation 3
// figure manip3_reponse_indicielle_P
figure correcteur prop

#figure(
  image("figures2/correcteurr_p.png", width: 100%),
  caption: [Réponse indicielle du correcteur proportionnel],
) <fig-manip3_reponse_indicielle_P>


On prend $K_1=2/G_0=1,65$
 - $V_"0,63%"=0.63(V_"final"-V_"initial")+V_"initial"=0.32$ V
 - $tau_P=$20,59 ms < $tau = 56,14$ ms
 - $H_0=0,65$
Le correction permet d'augmenter la rapidité du système.

= Préparation 5
\
 - Pour  compenser le pôle dominant, il faut prendre#space#space#result[$"GT"_i=tau$]
\Pour cette caleur de $G dot T_i$ on a:
\
 - #result[$T_"BF" (p)=1/(1+T_i /(K G_0)p)$]
\
 - #result[$t_(r,5%) = (3T_i)/(K G_0)$]
\
 - #result[$K_2 = (3T_i)/(tau G_0) = 4,64 "pour " T_i=0,1$s]
 \
 - #result( $G_2=tau/T_i = 0,56 "pour" T_i=0,1 $)s

= Manipulation 4
// figure manip4_reponse_indicielle_PI
#figure(
  image("figures2/correcteur_pi_2.png", width: 100%),
  caption: [Réponse indicielle du correcteur proportionnel-intégral ],
) <fig-manip4_reponse_indicielle_PI>
On prend $T_i=0,1s$ s, $G=0,56$ et $K_2=4,46$
 - $V_"final"=1$ V
 - $V_"initial"=-1$
 - $0,63(V_"final"-V_"initial")+V_"initial"=0,26$ V
 - $tau_"PI"=19$ ms
 - $H_0=1,19$
 - $epsilon_s=0" rad" dot s^(-1) dot V^(-1)$

Théoriquement $cases(H_0=1, tau_"PI"=T_i/(K_2G_0)=18" ms")$

== Influence d'une mauvaise compensation de pôle dominant

Au lieu de prendre  $G=4,46$ on prend $G=0.18$.
On obtient la réponse indicielle:
// figure manip4_influence_mauvaise_compensation_pole_dom
figure
/*
#figure(
  image("./figures/manip4_influence_mauvaise_compensation_pole_dom.png", width: 100%),
  caption: [Réponse indicielle du PI avec mauvaise compensation de pôle $cases("jaune → entrée "x_c, "orange → sortie "#s)$],
) <fig-manip4_influence_mauvaise_compensation_pole_dom>
*/

On observes des oscillations caractéristiques d'un deuxième ordre.

= Préparation 6
== Correcteur proportionnel
\
Pour satisfaire le cahier des charges défini précédemment on prend $C(p) = G_0/2$, on a donc:
\

#result[$((Delta Omega_b (p))/B(p))_(X_c (p) =0)=1/3(1+tau p)/(1+tau/3 p)$]

#figure(
  callisto.display("fig-reg-prop", nb: json("code.ipynb")),
  caption: [Diagramme de Bode en gain]
) <fig-reg-prop>


== Correcteur proportionnel-intégral
Pour satisfaire le le cahier des charges défini précédemment on prend $C(p) = K_2 (G_2 + 1/T_i p)$ avec 
 - $K_2 = (3T_i)/(tau G_0)$

 - $G_2=tau/T_i$

On a donc: #space #result[$(Delta Omega_b (p))/B(p)=1/3 (tau p)/(1+tau/3 p)$]

#figure(
  callisto.display("fig-reg-prop-integ", nb: json("code.ipynb")),
  caption: [Diagramme de Bode en gain]
) <fig-reg-prop-integ>


= Manipulation 5
== Rejection de la perturbation du correcteur P
// figure manip5_reponse_sinus_P

#figure(
  image("figures2/perturbation_proportionnel .png", width: 100%),
  caption: [Réponse en régulation du proportionnel avec perturbation],
) <fig-manip5_reponse_sinus_P> 

On voit que le bruit statique n'est pas totalement rejetté ($7,5$ dB), le rejet de la perturbation à 3Hz est de $6$ dB.


== Rejection de bruit du correcteur PI

// figure manip5_reponse_sinus_PI


#figure(
  image("figures2/perturbation_prop_integ.png", width: 100%),
  caption: [Réponse en régulation du proportionnel-intégral avec perturbation],
) <fig-manip5_reponse_sinus_PI>
On voit que lcomposante statique est totalement rejettée, le rejet de la perturbation à 3Hz est de $4$ dB.


= Conclusion

Que ce soit en régulation ou en asservissement, le correcteur proportionnel-intégral est meilleur que le correcteur proportionnel vis-àvis de la consigne et de la perturbation.
