from .base import BaseAgent


class AdministrationAgent(BaseAgent):
    key = "administration"
    title = "ADMINISTRATION IA"
    subject = "l'administration de DMS / YouGoo"
    empty_message = "Aucune demande administrative."
    role_prompt = (
        "Tu aides pour les documents, courriers, devis, factures, échéances et le classement. "
        "Tu ne remplaces pas l'expert-comptable."
    )
    domains = [
        "Documents",
        "Dossiers",
        "Courriers",
        "Échéances",
        "Contrats",
        "Organisation administrative",
        "Classement",
        "Suivi des pièces",
    ]
    plan = [
        "Identifier le document ou dossier concerné.",
        "Vérifier les informations nécessaires.",
        "Identifier les échéances.",
        "Organiser les documents.",
        "Signaler les éléments manquants.",
        "Présenter les actions à la direction.",
    ]
    validation = (
        "Les documents officiels et décisions importantes\n"
        "doivent être validés par la direction."
    )
