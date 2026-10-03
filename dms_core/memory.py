"""Mémoire locale de DMS : faits durables et notes de décision (fichier JSON).

Règle : n'y mettre AUCUNE donnée de santé ni donnée identifiante de client.
Le fichier est dans dms_core/data/ (ignoré par git).
"""
import json
from datetime import datetime
from pathlib import Path


class Memory:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().parent / "data" / "memory.json"
        self._data = {"facts": {}, "notes": []}
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass  # fichier illisible : on repart d'une mémoire vide sans l'écraser avant la prochaine écriture

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def remember(self, key, value):
        """Enregistre un fait durable (ex. 'zone' -> 'Sud-Ouest marnais')."""
        self._data["facts"][key] = value
        self._save()

    def add_note(self, text, agent=""):
        """Ajoute une note datée (décision, point à suivre)."""
        self._data["notes"].append(
            {"date": datetime.now().isoformat(timespec="minutes"), "agent": agent, "text": text}
        )
        self._data["notes"] = self._data["notes"][-50:]
        self._save()

    def context(self, max_notes=10):
        """Texte à injecter dans les consignes d'un agent."""
        lines = [f"- {k} : {v}" for k, v in self._data["facts"].items()]
        notes = self._data["notes"][-max_notes:]
        lines += [f"- ({n['date']}) {n['text']}" for n in notes]
        return "\n".join(lines) if lines else "(mémoire vide)"
