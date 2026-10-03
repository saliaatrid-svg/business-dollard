# L'équipe d'agents de DMS : tableau unique

Un seul jeu d'agents, avec les mêmes prénoms partout : dans Claude Code (`.claude/agents/`), dans le code Python (`dms_core/`) et au téléphone (`phone-agent/`).

| Prénom | Rôle | Agent Claude Code | Classe Python | Avatar |
| --- | --- | --- | --- | --- |
| Camille | Directrice de pilotage, répartit les demandes | `dms-directeur` | `Orchestrator` | `docs/avatars/camille.jpg` |
| Alix | Stratégie, offre, partenaires, concurrence | `dms-strategie` | `StrategieAgent` | `docs/avatars/alix.jpg` |
| Sacha | Marketing et acquisition de clients | `dms-marketing` | `CommercialAgent` | `docs/avatars/sacha.jpg` |
| Noa | Contenu et communication | `dms-contenu` | `CommunicationAgent` | `docs/avatars/noa.jpg` |
| Maël | Administratif et comptabilité | `dms-admin-compta` | `AdministrationAgent` | `docs/avatars/mael.jpg` |
| Lou | Juridique, RGPD, réglementation | `dms-juridique-rgpd` | `JuridiqueAgent` | `docs/avatars/lou.jpg` |
| Robin | Ressources humaines | `dms-rh` | `RHAgent` | à générer (prompt n° 8, `docs/avatars-gemini.md`) |
| Morgan | Opérations : planning, interventions, accompagnements | `dms-operations` | `OperationsAgent` | à générer (prompt n° 9, `docs/avatars-gemini.md`) |
| Charlie | Accueil téléphonique | `dms-accueil-telephone` | service `phone-agent/` (Node) | `docs/avatars/charlie.jpg` |

## Qui fait quoi, selon l'outil
- **Dans Claude Code** (conversation) : on s'adresse à un agent par son nom, ils préparent des brouillons.
- **En ligne de commande Python** : `python -m dms_core "demande"` ; Camille choisit l'agent. Les réponses sont structurées (demande, analyse, validation, statut).
- **Au téléphone** : Charlie répond aux appels via Twilio (voir `phone-agent/README.md`). Son pendant Claude Code sert à préparer ses scripts.

## Règles communes à tous
1. La présidente valide avant tout envoi, toute publication, toute signature, tout paiement.
2. Aucune donnée de santé ni donnée identifiante de client dans les échanges avec les agents.
3. Tarifs : seule la garde de nuit (215 € TTC) peut être annoncée par Charlie ; tout le reste est à confirmer.
4. Les agents sont des assistants virtuels : mention « assistant virtuel (IA) » à tout usage public, aucun titre ou diplôme inventé.
5. Contexte et style communs : `docs/dms-contexte.md`, `docs/guide-de-style.md`, `docs/charte-marque.md`.

## Ce qui reste à faire pour finir le rapprochement
- Générer les avatars de Robin et de Morgan (prompts n° 8 et 9).
- Brancher d'autres canaux sur le même `Orchestrator` si besoin (message Slack, courriel), après validation RGPD.
- Fusionner le reste de vos fichiers Python (mémoire, fichier principal) si vous les récupérez depuis votre ordinateur.
