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

// bloc de warning
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
    color: black,
    radius: 4pt,
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
  *TP4-5 - 231 - Mini projet VGA*
])
#grid(
  columns: (1fr, 1fr),
  align(center)[
    Scott Hamilton \
    // École Normale Supérieure Paris-Saclay \
    // #link("mailto:scott.hamilton@ens-paris-saclay.fr")
  ],
  align(center)[
    Ibrahim El Kassimi
    // École Normale Supérieure Paris-Saclay \
    // #link("mailto:ibrahim.elkassimi@ens-paris-saclay.fr")
  ]
)
#align(center)[
  #set par(justify: false)
]

// pour la numérotation des sections
#set align(left)
#set heading(numbering: "1.")
#counter(heading).update(0)

// pour la table des matières
#outline()

///// Fin Title Page /////

#pagebreak()

= Introduction
Ces deux séances de TP nous ont permis de prendre en main un contrôleur VGA à l'aide du langage VHDL et de la carte Basys2, puis afficher un jeu de Pong.

= Implémentation d'un contrôleur VGA
Après avoir configuré et testé le contrôleur VGA, il a été possible d'afficher un drapeau ainsi qu'un rectangle, avec la possibilité de modifier les couleurs affichées en appuyant sur un bouton.
#figure(image("figures/rectangle.jpg", width: 50%),
        caption:[Affichage d'un rectangle avec possibilité de modifier sa couleur via un bouton

])

= Mise en œuvre du jeu "Pong"
Pour la réalisation du jeu « PONG », nous avons conservé le drapeau en arrière-plan tout en intégrant et la logique du jeu par-dessus cet affichage.
#figure(image("figures/pong.jpg", width: 50%),    
        caption:[Affichege du jeu "PONG"]) 
= Conclusion
Ce TP nous a permis de concevoir des modules VHDL pour afficher à la fois des images statiques et dynamiques sur un écran VGA.  