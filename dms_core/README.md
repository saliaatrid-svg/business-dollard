# dms_core : agents IA de DMS en Python

Intègre vos classes `RHAgent`, `AdministrationAgent`, `CommercialAgent` et `CommunicationAgent` (même structure, mêmes domaines, mêmes plans, mêmes règles de validation), branchées sur Claude. Ajouts : `JuridiqueAgent`, une mémoire (`Memory`) et un chef d'orchestre (`Orchestrator`).

## Utiliser
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...            # sans clé : modèle fixe, signalé comme tel
python -m dms_core "Écrire un post Facebook pour YouGoo"
python -m dms_core "Quel consentement pour une photo ?" --agent juridique
python -m dms_core "Recruter un intervenant de nuit" --note "Priorité : nuits du week-end"
python -m unittest discover -s tests    # 13 tests, sans réseau
```

Dans le code :
```python
from dms_core import Memory, Orchestrator
key, reponse = Orchestrator(Memory()).handle("Préparer un devis de nuit")
```

## Ce qui a changé par rapport à vos fichiers
- Chaque agent répond vraiment (via Claude) avec le contexte `docs/dms-contexte.md` et le style `docs/guide-de-style.md`. Le cadre « DEMANDE / ANALYSE / VALIDATION / STATUT » est conservé.
- Sans clé API ou en cas de panne, il renvoie votre modèle fixe, avec un statut honnête : « aucune IA utilisée, la demande n'a pas été analysée » (l'ancien « Analyse locale effectuée » laissait croire à une analyse).
- `memory` sert maintenant : faits durables et notes, injectés dans les consignes. Elle est stockée dans `dms_core/data/` (ignoré par git) : n'y mettez aucune donnée de santé.
- Garde-fou : une demande qui contient un numéro de sécurité sociale ou un IBAN n'est **pas envoyée** à l'IA.
- Aucun agent n'envoie, ne publie ni ne signe quoi que ce soit : ils produisent des brouillons que la direction valide.

## Réglages (variables d'environnement)
- `DMS_MODEL` : modèle des agents (défaut `claude-sonnet-5-5`).
- `DMS_ROUTER_MODEL` : modèle du choix d'agent (défaut `claude-haiku-4-5-20251001`).
