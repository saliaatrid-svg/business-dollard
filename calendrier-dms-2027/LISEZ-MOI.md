# Calendrier DMS 2027

- `Calendrier_DMS_2027.pdf` : calendrier mural, 14 pages A4 paysage (couverture, 12 mois, dos).
- `Calendrier_DMS_2027.html` : fichier source (modifiable).
- `outil/build_calendrier.py` : script qui régénère le calendrier.
  `python3 build_calendrier.py logo.png sortie.html [dossier_photos]`
  puis impression PDF avec Chromium (`--headless --print-to-pdf`).
  Le logo (`logo simple entreprise.png.png`) est dans le Drive DMS.

## Illustrations

Chaque mois montre une activité de services à la personne en dessin animé (garde d'enfants, ménage,
repassage, jardinage, repas, courses, accompagnement en voiture, trajets des enfants, veille sur la maison,
présence de nuit, sorties accompagnées, équipe). Elles sont générées par `outil/illus2.py`
(`python3 illus2.py dossier_svg`, à lancer depuis le dossier `outil`, qui utilise `illus.py`).
Commande complète : `python3 build_calendrier.py logo.png sortie.html dossier_photos dossier_svg`.
Une photo `NN.jpg` du dossier photos remplace l'illustration du mois correspondant.

## Ajouter des photos (une par mois)

Dossier de photos : `01.jpg` (janvier) à `12.jpg` (décembre), format paysage, au moins 1500 px de large,
et un fichier `credits.txt` avec une ligne par photo : `mois|auteur|licence et source`, par exemple :
`07|Prénom Nom|CC BY 4.0, Wikimedia Commons`

Idées de thèmes sans visage reconnaissable : 1 galette des rois ou flocons, 2 crêpes ou perce-neige,
3 jonquilles ou mimosa, 4 cerisiers en fleurs, 5 muguet, 6 roses ou lavande, 7 champ de tournesols,
8 champ de blé, 9 vignes de Champagne (vendanges), 10 feuilles d'automne, 11 forêt dans la brume, 12 sapin de Noël.

Règles : aucune photo d'un client ou d'un bénéficiaire ; accord écrit pour toute personne reconnaissable ;
licence vérifiée (Unsplash+ est payant : ne pas l'utiliser) ; crédits imprimés au dos du calendrier.
