import os

from .agents import AGENTS
from .agents.base import default_client, frame

KEYWORDS = {
    "juridique": ["rgpd", "cnil", "contrat", "cgv", "consentement", "juridique", "mention légale", "loi", "agrément"],
    "rh": ["recrut", "intervenant", "embauche", "formation", "salari", "planning équipe", "cdi", "cdd"],
    "communication": ["facebook", "instagram", "post", "flyer", "affiche", "publication", "vidéo", "campagne", "newsletter"],
    "commercial": ["prospect", "client", "devis", "prescripteur", "yougoo", "clic", "carsat", "relance"],
    "strategie": ["stratégie", "offre", "tarif", "concurren", "positionnement", "territoire", "partenariat", "développer"],
    "administration": ["document", "courrier", "facture", "échéance", "dossier", "classement", "urssaf", "compta"],
}


def keyword_route(request):
    text = request.lower()
    scores = {k: sum(w in text for w in words) for k, words in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "administration"


class Orchestrator:
    prenom = "Camille"
    avatar = "docs/avatars/camille.jpg"
    """Choisit l'agent adapté à une demande puis la lui transmet."""

    def __init__(self, memory, client=None):
        self.memory = memory
        self.client = client if client is not None else default_client()
        self.router_model = os.environ.get("DMS_ROUTER_MODEL", "claude-haiku-4-5-20251001")
        self.agents = {k: cls(memory, self.client) for k, cls in AGENTS.items()}

    def route(self, request):
        if self.client is not None:
            try:
                response = self.client.messages.create(
                    model=self.router_model,
                    max_tokens=10,
                    system=(
                        "Tu classes une demande destinée à une société de services à la personne. "
                        f"Réponds par un seul mot parmi : {', '.join(self.agents)}."
                    ),
                    messages=[{"role": "user", "content": request}],
                )
                answer = "".join(b.text for b in response.content if getattr(b, "type", "text") == "text")
                answer = answer.strip().lower()
                if answer in self.agents:
                    return answer
            except Exception:
                pass  # on retombe sur les mots-clés
        return keyword_route(request)

    def handle(self, request, agent=None):
        request = request.strip()
        if not request:
            return "", frame("DMS IA", "Aucune demande.")
        key = agent if agent in self.agents else self.route(request)
        return key, self.agents[key].analyze(request)
