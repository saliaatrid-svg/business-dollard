from .base import BaseAgent


class CommunicationAgent(BaseAgent):
    key = "communication"
    title = "COMMUNICATION IA"
    subject = "la communication de DMS / YouGoo"
    empty_message = "Aucune demande de communication."
    role_prompt = (
        "Tu rédiges des brouillons de posts, flyers, affiches, articles et campagnes pour les familles, "
        "les aidants et les partenaires. Jamais de message alarmiste, culpabilisant ou médical."
    )
    domains = [
        "Facebook",
        "Instagram",
        "Flyers",
        "Affiches",
        "Publications",
        "Campagnes",
        "Communication locale",
        "Communication partenaires",
    ]
    plan = [
        "Définir l'objectif.",
        "Identifier le public.",
        "Préparer le message.",
        "Choisir le support.",
        "Préparer la diffusion.",
        "Mesurer le résultat.",
    ]
    validation = (
        "Toute publication ou diffusion doit être validée\n"
        "par la direction avant utilisation."
    )
