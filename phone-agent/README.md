# Agent téléphonique DMS (Charlie)

Charlie répond aux appels de **DMS - De la Mémoire aux Soins** : elle répond aux questions fréquentes, prend des messages et enregistre des demandes de rendez-vous dans l'agenda Google.

```
Appelant ──> numéro Free ──(renvoi d'appel)──> numéro Twilio
                                                   │  POST /voice (signature vérifiée)
                                                   ▼
                              ce serveur ──> TwiML <ConversationRelay>
                                                   │  WebSocket /relay (jeton signé)
                                                   ▼
                        Twilio : voix -> texte    Claude    texte -> voix
                                                   │ outils
                          ┌──────────────┬─────────┴──────────┬────────────────┐
                    save_message   request_appointment   alert_urgent   refuse_transcription
                    (fichier local  (Google Agenda,      (Slack)        (rien n'est conservé)
                     + Slack)        créneau « à confirmer »)
```

Ce qui est prévu et ce qui ne l'est pas :

- Charlie **ne confirme jamais** un rendez-vous : l'événement est créé en « provisoire » (`À confirmer`) et la responsable rappelle.
- Elle n'annonce **aucun tarif** tant que `config/dms-info.md` n'en contient pas.
- Urgence : elle dit d'appeler le 15 / 112 (3114 pour une détresse morale) et prévient Slack.
- Slack ne reçoit **jamais de détail de santé** : seulement nom, numéro, motif (catégorie), urgence. Le détail reste dans `data/` sur le serveur.
- Elle dit d'emblée que l'appel est transcrit et que c'est un assistant virtuel.

> Le code est testé par des tests automatiques (`npm test`) mais **n'a pas été essayé avec une vraie ligne**. Faites plusieurs appels d'essai avant de tout renvoyer vers Charlie, et vérifiez les points marqués « à vérifier » ci-dessous.

## 1. Ce dont vous avez besoin

| Élément | Pourquoi | Où |
| --- | --- | --- |
| Clé API Anthropic | Le « cerveau » de Charlie | console.anthropic.com |
| Compte Twilio + numéro français | Reçoit l'appel, gère la voix | twilio.com |
| Un serveur en HTTPS avec WebSocket | Fait tourner ce code | voir §4 |
| Agenda Google + compte de service (facultatif) | Créneaux et rendez-vous | Google Cloud Console |
| Webhook Slack entrant (facultatif) | Notifications | Slack > Apps > Incoming Webhooks |

Sans agenda Google, Charlie prend simplement un message pour les demandes de rendez-vous.

## 2. Twilio

1. Créez un compte, puis achetez un numéro français. **À vérifier** : la France exige en général un dossier réglementaire (adresse, justificatif de l'entreprise) avant l'activation d'un numéro.
2. Dans la configuration du numéro, rubrique « A call comes in » : `Webhook`, `HTTP POST`, URL `https://VOTRE-SERVEUR/voice`.
3. Notez le **Auth Token** (Console Twilio) : c'est `TWILIO_AUTH_TOKEN`.
4. **À vérifier** : les options de ConversationRelay (`language`, `ttsProvider`, `transcriptionProvider`, `voice`) et les voix françaises disponibles dans la documentation Twilio actuelle. Elles se règlent avec `TTS_PROVIDER`, `TTS_VOICE`, `STT_PROVIDER`.

## 3. Renvoyer votre numéro Free vers Twilio

Choisissez d'abord un renvoi **sur non-réponse ou occupation** pendant les essais, puis inconditionnel une fois satisfait·e.

- **Free Mobile** (codes standard GSM, **à vérifier** sur votre abonnement) : `**21*+33XXXXXXXXX#` puis appel = renvoi de tous les appels ; `##21#` pour l'annuler. Renvoi sur non-réponse : `**61*+33XXXXXXXXX#`.
- **Freebox (ligne fixe)** : le renvoi se règle dans l'espace abonné Free ou depuis le téléphone, selon le modèle.

Vous voulez qu'elle réponde « tout le temps » : utilisez le renvoi inconditionnel. Vous ne pourrez alors plus décrocher vous-même sur ce numéro : donnez-vous un second numéro pour les urgences ou testez d'abord en renvoi sur non-réponse.

## 4. Installer et lancer

```bash
cd phone-agent
npm install
cp .env.example .env     # puis remplissez les valeurs
npm test                 # 8 tests automatiques
npm start
```

Variables obligatoires : `ANTHROPIC_API_KEY`, `TWILIO_AUTH_TOKEN`, `PUBLIC_URL` (l'adresse HTTPS publique, sans `/` final), `SIGNING_SECRET` (`openssl rand -hex 32`).

Pour un essai depuis chez vous, exposez le port avec un tunnel HTTPS (par exemple ngrok ou Cloudflare Tunnel) et mettez son adresse dans `PUBLIC_URL` et dans Twilio.

**Hébergement définitif** : un petit serveur (VPS ou plateforme d'hébergement d'applications) **situé dans l'Union européenne**, avec HTTPS, WebSocket et un disque chiffré pour `data/`. L'application n'a besoin que de Node 20+.

## 5. Contenu à personnaliser

- `config/dms-info.md` : **c'est la seule source d'informations de Charlie**. Remplissez tous les `[À COMPLÉTER]` : communes, prestations, horaires de rappel, premier rendez-vous. Ne mettez aucun tarif si vous ne voulez pas qu'elle en cite.
- `.env` : `BUSINESS_HOURS` (jours et heures des rendez-vous), `APPOINTMENT_MINUTES`, `MIN_NOTICE_HOURS` (préavis minimum, 24 h par défaut).
- Agenda Google : créez un compte de service, téléchargez sa clé JSON (`GOOGLE_SERVICE_ACCOUNT_FILE`), **partagez votre agenda avec l'adresse du compte de service** (droit « Apporter des modifications aux événements ») et renseignez `GOOGLE_CALENDAR_ID`.

## 6. Checklist RGPD (à faire valider avec `dms-juridique-rgpd` et, en cas de doute, la CNIL ou un juriste)

Les appels de familles et d'aidants peuvent révéler des **données de santé** (article 9 du RGPD, catégorie particulière).

- [ ] **Information de l'appelant** : l'annonce d'accueil dit qu'il s'agit d'une assistante virtuelle et que l'appel est transcrit. Complétez avec une politique de confidentialité en ligne (finalité, durée, droits, contact) et donnez-en l'adresse sur demande.
- [ ] **Refus** : si l'appelant refuse la transcription, aucune transcription n'est conservée. Le message reste enregistré s'il demande à être rappelé (il faut bien son numéro).
- [ ] **Base légale et finalité** : tenez à jour le registre des traitements (Lou peut le préparer).
- [ ] **Minimisation** : Charlie ne demande ni détail de santé, ni adresse complète.
- [ ] **Durée de conservation** : 30 jours par défaut (`RETENTION_DAYS`), purge automatique au démarrage puis chaque jour. Ajustez selon votre analyse.
- [ ] **Sous-traitants** : contrat de sous-traitance (DPA) avec Twilio, Anthropic, Slack, Google, et l'hébergeur. Vérifiez où sont traitées et stockées les données (transferts hors UE, clauses contractuelles types).
- [ ] **Hébergement de données de santé (HDS)** : demandez à un juriste ou à la CNIL si votre usage impose un hébergeur certifié HDS. Ne présumez pas de la réponse.
- [ ] **Sécurité** : disque chiffré, accès restreint au dossier `data/` (fichiers créés en mode 0600), `.env` jamais commité.
- [ ] **Droits des personnes** : procédure pour retrouver et supprimer un message ou une transcription sur demande (les fichiers sont nommés par identifiant de message et par identifiant d'appel).
- [ ] **Analyse d'impact (AIPD)** : à envisager, car le traitement peut concerner des personnes vulnérables et des données de santé.

## 7. Structure du code

| Fichier | Rôle |
| --- | --- |
| `src/index.js` | Serveur HTTP `/voice`, `/health`, WebSocket `/relay` |
| `src/security.js` | Signature Twilio et jeton du WebSocket |
| `src/twiml.js` | Réponse TwiML et annonce d'accueil |
| `src/session.js` | Une session par appel : dialogue en flux avec Claude, coupure de parole |
| `src/prompt.js` | Consignes de Charlie |
| `src/tools.js` | Outils : message, disponibilités, rendez-vous, urgence, refus, fin d'appel |
| `src/slots.js` | Calcul des créneaux (fuseau Europe/Paris) |
| `src/calendar.js` | Google Agenda |
| `src/store.js` | Fichiers JSON locaux et purge |
| `src/notify.js` | Slack |
| `config/dms-info.md` | Informations sur DMS (à compléter) |

## 8. Limites connues

- Non essayé sur une vraie ligne : latence, qualité de la voix et fin d'appel (l'outil `end_call` peut couper la dernière phrase) sont à valider en appelant.
- Stockage sur fichiers locaux : sur un hébergeur à disque éphémère, il faut monter un volume.
- Un seul serveur, pas de reprise d'appel en cas de redémarrage.
- Le renvoi d'appel vers un humain n'est pas implémenté : Charlie prend un message et prévient Slack.
