# Avatars animés : courts films avec voix (usage interne)

Objectif : pour chaque agent, un clip d'environ 8 secondes où le personnage bouge et **parle en français**, dans un style film d'animation chaleureux.

## État au 4 octobre 2026
- L'outil de vidéo connecté (vidIQ) sait générer des clips avec voix à partir d'un texte et d'images de référence (modèles Veo 3.1, Kling, Seedance, entre autres). Les portraits de `docs/avatars/` peuvent servir de références pour garder le même personnage.
- **Blocage : crédits.** Il reste 1 crédit, le renouvellement (150 crédits) est prévu le 9 octobre 2026. Le coût exact d'un clip n'est pas connu avant de le lancer : il dépend du modèle et de la durée. À vérifier alors, avant tout lancement.
- La qualité de la voix française et de la synchronisation des lèvres n'est pas garantie : à tester d'abord sur **un seul agent** (Camille).

## Deux styles possibles
1. **Réaliste** : on utilise les portraits actuels (photos de personnages inventés). Le résultat ressemble à une vraie personne qui parle : à réserver à l'usage interne, avec la mention « assistant virtuel (IA) ».
2. **Film d'animation** (ce que vous demandez) : il faut d'abord de nouveaux portraits illustrés en 3D. À générer dans Gemini avec le bloc ci-dessous, puis à utiliser comme images de référence.

### Bloc de style « film d'animation » (à coller dans Gemini, avant le prompt de chaque personnage)
```
Transforme ce personnage en personnage de film d'animation 3D chaleureux : visage expressif et doux, grands yeux, textures de tissu soignées, éclairage de fenêtre doux, fond blanc cassé avec une légère teinte lavande et touches dorées. Garde exactement la coiffure, les vêtements et les traits principaux de la photo jointe. Aucun texte, aucun logo.
```
(Joindre la photo du personnage concerné.)

## Prompts de clips (8 secondes, une réplique chacun)
Modèle de prompt pour l'outil de vidéo, avec le portrait du personnage en image de référence :
```
Court film d'animation 3D chaleureux, plan fixe poitrine, le personnage de l'image de référence regarde la caméra et dit en français, avec une voix <VOIX> : « <RÉPLIQUE> ». Léger mouvement de tête, clignements naturels, sourire bienveillant, lèvres synchronisées avec la parole. Décor identique à l'image. Pas de musique, pas de texte à l'écran.
```

| Agent | Voix | Réplique |
| --- | --- | --- |
| Camille | féminine, posée, chaleureuse | Bonjour, je suis Camille, l'assistante virtuelle de DMS. Je coordonne l'équipe et je prépare votre semaine. |
| Alix | masculine, calme, réfléchie | Bonjour, je suis Alix, assistant virtuel. J'aide DMS à choisir où concentrer ses efforts sur le territoire. |
| Sacha | féminine, dynamique, souriante | Bonjour, je suis Sacha, assistante virtuelle. Je fais connaître DMS et YouGoo aux familles et aux aidants. |
| Noa | masculine, légère, créative | Bonjour, je suis Noa, assistant virtuel. J'écris vos posts et vos vidéos, et c'est vous qui validez. |
| Maël | masculine, grave, rassurante | Bonjour, je suis Maël, assistant virtuel. Je suis vos échéances et vos factures, pour que rien ne vous échappe. |
| Lou | féminine, claire, sérieuse | Bonjour, je suis Lou, assistante virtuelle. Je veille au RGPD, parce que les données de santé se protègent avec soin. |
| Robin | neutre, attentive | Bonjour, je suis Robin, assistant virtuel. Je prépare vos recrutements, sans jamais décider à votre place. |
| Morgan | neutre, organisée | Bonjour, je suis Morgan, assistant virtuel. J'organise le planning des nuits et des accompagnements. |
| Charlie | féminine, douce, lente | Bonjour, je suis Charlie, assistante virtuelle. Je prends vos messages et je vous oriente vers une personne quand il le faut. |

## Marche à suivre (à partir du 9 octobre)
1. Vérifier le solde de crédits (gratuit).
2. Générer **un seul** clip de test (Camille), dire le coût avant de lancer, et juger la voix et les lèvres.
3. Si le résultat convient, lancer les autres un par un, en annonçant le coût total avant.
4. Ne jamais relancer un clip déjà livré sans accord : chaque lancement est facturé.

## Précautions
- Visages et voix inventés : aucune ressemblance voulue avec une personne réelle ; ne pas demander « la voix de » quelqu'un.
- Mention « assistant virtuel (IA) » pour tout usage en dehors de DMS.
- Les personnages ne portent aucun titre de métier de santé.
