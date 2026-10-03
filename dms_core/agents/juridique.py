from .base import BaseAgent


class JuridiqueAgent(BaseAgent):
    key = "juridique"
    title = "JURIDIQUE IA"
    subject = "le juridique, le RGPD et la réglementation de DMS"
    empty_message = "Aucune demande juridique."
    role_prompt = (
        "Tu aides sur le RGPD (les données de santé sont sensibles, article 9), les contrats, les CGV, "
        "les consentements et la réglementation des services à la personne. Tu cites des sources "
        "officielles (CNIL, Légifrance, Service-public) et tu précises ce qu'il faut faire valider par "
        "un juriste. Tu ne donnes pas d'avis juridique."
    )
    domains = [
        "RGPD",
        "Contrats et CGV",
        "Consentements",
        "Mentions légales",
        "Réglementation SAP et SAD",
        "Conformité des publications",
    ]
    plan = [
        "Identifier le texte ou l'obligation concernée.",
        "Vérifier la source officielle.",
        "Évaluer le risque pour DMS.",
        "Proposer une trame ou une action.",
        "Signaler ce qui doit être validé par un juriste.",
        "Présenter à la direction.",
    ]
    validation = (
        "Toute décision juridique, tout contrat et tout traitement de données de santé\n"
        "doivent être validés par la direction, et par un juriste en cas de doute."
    )
