import os
import re
from pathlib import Path

LINE = "=" * 60
DOCS = Path(__file__).resolve().parents[2] / "docs"

SENSITIVE = [
    (re.compile(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}(\s?\d{2})?\b"), "un numéro de sécurité sociale"),
    (re.compile(r"\bFR\d{2}(?:\s?\d{4}){5}\s?\d{3}\b", re.I), "un IBAN"),
]


def sensitive_identifier(text):
    """Renvoie le type d'identifiant sensible trouvé dans le texte, sinon None."""
    for pattern, label in SENSITIVE:
        if pattern.search(text):
            return label
    return None


def default_client():
    """Client Claude si la clé API et le paquet sont disponibles, sinon None."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
    except ImportError:
        return None
    return anthropic.Anthropic()


def read_doc(name):
    try:
        return (DOCS / name).read_text(encoding="utf-8")
    except OSError:
        return ""


def frame(title, body):
    return f"{LINE}\n{title.center(60).rstrip()}\n{LINE}\n\n{body}\n\n{LINE}"


class BaseAgent:
    key = ""
    prenom = ""
    avatar = ""
    title = ""
    subject = ""
    domains = []
    plan = []
    validation = ""
    role_prompt = ""
    empty_message = "Aucune demande."

    def __init__(self, memory, client=None, model=None):
        self.memory = memory
        self.client = client if client is not None else default_client()
        self.model = model or os.environ.get("DMS_MODEL", "claude-sonnet-5-5")

    @property
    def header(self):
        return f"{self.title} ({self.prenom})" if self.prenom else self.title

    # --- consignes envoyées à Claude ---
    def system_prompt(self):
        domains = "\n".join(f"- {d}" for d in self.domains)
        plan = "\n".join(f"{i}. {p}" for i, p in enumerate(self.plan, 1))
        return (
            f"Tu t'appelles {self.prenom or self.title}. Tu es l'agent « {self.title} » de DMS - De la Mémoire aux Soins (Sézanne, Marne), "
            f"société de services à la personne. {self.role_prompt}\n\n"
            f"Domaines couverts :\n{domains}\n\nPlan de travail habituel :\n{plan}\n\n"
            "Règles :\n"
            "- Réponds en français, de façon concrète et structurée : Analyse, Actions proposées, "
            "Informations manquantes, Points à faire valider.\n"
            f"- {self.validation.replace(chr(10), ' ')}\n"
            "- N'invente aucun chiffre, tarif, délai, texte de loi ou information absente du contexte : "
            "dis ce qui manque.\n"
            "- Aucune donnée de santé ni donnée identifiante de client : si on t'en donne, ne les répète pas.\n"
            "- Tu prépares des brouillons et des propositions, tu n'envoies, ne publies et ne signes rien.\n\n"
            f"CONTEXTE DMS :\n{read_doc('dms-contexte.md')}\n\n"
            f"GUIDE DE STYLE :\n{read_doc('guide-de-style.md')}\n\n"
            f"MÉMOIRE :\n{self.memory.context()}"
        )

    def ask(self, request):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt(),
            messages=[{"role": "user", "content": request}],
        )
        return "".join(b.text for b in response.content if getattr(b, "type", "text") == "text").strip()

    # --- rendu ---
    def render(self, request, analysis, status):
        body = (
            f"DEMANDE :\n{request}\n\nANALYSE :\n{analysis}\n\n"
            f"VALIDATION :\n{self.validation}\n\nSTATUT :\n{status}"
        )
        return frame(self.header, body)

    def local(self, request, note=""):
        domains = "\n".join(f"- {d}" for d in self.domains)
        plan = "\n".join(f"{i}. {p}" for i, p in enumerate(self.plan, 1))
        analysis = (
            f"Cette demande concerne {self.subject}.\n\nDOMAINES :\n{domains}\n\nPLAN D'ACTION :\n{plan}"
        )
        status = "Modèle fixe : aucune IA utilisée, la demande n'a pas été analysée."
        if note:
            status += f" {note}"
        return self.render(request, analysis, status)

    def analyze(self, request):
        request = request.strip()
        if not request:
            return self.empty_message
        found = sensitive_identifier(request)
        if found:
            return frame(
                self.header,
                f"Demande non traitée : elle contient {found}. Retirez cette donnée "
                "puis reformulez avec des initiales ou un cas anonymisé.",
            )
        if self.client is None:
            return self.local(request, "Définir ANTHROPIC_API_KEY pour activer l'IA.")
        try:
            analysis = self.ask(request)
        except Exception as err:  # réseau, quota, clé invalide : on retombe sur le modèle fixe
            return self.local(request, f"IA indisponible ({type(err).__name__}).")
        return self.render(request, analysis, "Analyse IA effectuée. Brouillon à valider par la direction.")
