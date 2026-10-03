import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from dms_core import Memory, Orchestrator
from dms_core.agents import AGENTS, RHAgent
from dms_core.agents.base import sensitive_identifier
from dms_core.orchestrator import keyword_route


class FakeClient:
    """Imite client.messages.create sans réseau."""

    def __init__(self, text="Analyse simulée.", fail=False):
        self.calls = []
        self.text = text
        self.fail = fail
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        if self.fail:
            raise RuntimeError("panne simulée")
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.text)])


def memory():
    return Memory(Path(tempfile.mkdtemp()) / "memory.json")


class AgentTests(unittest.TestCase):
    def test_demande_vide(self):
        self.assertEqual(RHAgent(memory(), client=None).analyze("   "), "Aucune demande RH.")

    def test_sans_cle_modele_fixe_honnete(self):
        out = RHAgent(memory(), client=None).analyze("Recruter un intervenant de nuit")
        self.assertIn("aucune IA utilisée", out)
        self.assertNotIn("Analyse locale effectuée", out)

    def test_avec_ia(self):
        client = FakeClient("Voici l'analyse.")
        out = RHAgent(memory(), client=client).analyze("Recruter un intervenant de nuit")
        self.assertIn("Voici l'analyse.", out)
        self.assertIn("validée par la direction", out)
        self.assertIn("Analyse IA effectuée", out)
        system = client.calls[0]["system"]
        self.assertIn("DMS", system)
        self.assertIn("Aucune donnée de santé", system)

    def test_panne_ia_retombe_sur_modele_fixe(self):
        out = RHAgent(memory(), client=FakeClient(fail=True)).analyze("Recruter")
        self.assertIn("IA indisponible", out)

    def test_donnee_sensible_non_envoyee(self):
        client = FakeClient()
        out = RHAgent(memory(), client=client).analyze("Dossier de 1 85 05 51 123 456 78")
        self.assertIn("non traitée", out)
        self.assertEqual(client.calls, [])

    def test_detection_iban(self):
        self.assertEqual(sensitive_identifier("FR76 3000 6000 0112 3456 7890 189"), "un IBAN")
        self.assertIsNone(sensitive_identifier("Prévoir 3 nuits cette semaine"))

    def test_six_agents_avec_prenoms_et_avatars(self):
        self.assertEqual(
            set(AGENTS), {"rh", "administration", "commercial", "communication", "juridique", "strategie"}
        )
        prenoms = {cls.prenom for cls in AGENTS.values()}
        self.assertEqual(prenoms, {"Robin", "Maël", "Sacha", "Noa", "Lou", "Alix"})
        root = Path(__file__).resolve().parents[1]
        for cls in AGENTS.values():
            if cls.key != "rh":  # l'avatar de Robin reste à générer
                self.assertTrue((root / cls.avatar).exists(), cls.avatar)

    def test_prenom_dans_entete_et_consignes(self):
        agent = RHAgent(memory(), client=None)
        self.assertIn("RH IA (Robin)", agent.analyze("Recruter"))
        self.assertIn("Tu t'appelles Robin", agent.system_prompt())


class OrchestratorTests(unittest.TestCase):
    def test_mots_cles(self):
        self.assertEqual(keyword_route("Écrire un post Facebook sur YouGoo"), "communication")
        self.assertEqual(keyword_route("Quel consentement RGPD pour une photo ?"), "juridique")
        self.assertEqual(keyword_route("Recruter un intervenant"), "rh")
        self.assertEqual(keyword_route("blabla"), "administration")
        self.assertEqual(keyword_route("Analyser la concurrence et notre positionnement"), "strategie")

    def test_routage_ia_puis_agent(self):
        client = FakeClient("commercial")
        orch = Orchestrator(memory(), client=client)
        key, out = orch.handle("Préparer un devis")
        self.assertEqual(key, "commercial")
        self.assertEqual(len(client.calls), 2)  # une pour le routage, une pour l'agent
        self.assertIn("COMMERCIAL IA", out)

    def test_routage_ia_invalide_utilise_mots_cles(self):
        orch = Orchestrator(memory(), client=FakeClient("n'importe quoi"))
        key, _ = orch.handle("Quel contrat pour un intervenant ?")
        self.assertEqual(key, "juridique")

    def test_agent_force(self):
        key, _ = Orchestrator(memory(), client=None).handle("Bonjour", agent="rh")
        self.assertEqual(key, "rh")


class MemoryTests(unittest.TestCase):
    def test_persistance(self):
        path = Path(tempfile.mkdtemp()) / "m.json"
        Memory(path).remember("zone", "Sud-Ouest marnais")
        self.assertIn("Sud-Ouest marnais", Memory(path).context())

    def test_notes_limitees(self):
        m = memory()
        for i in range(60):
            m.add_note(f"note {i}")
        self.assertIn("note 59", m.context(max_notes=1))
        self.assertNotIn("note 0)", m.context(max_notes=100))


if __name__ == "__main__":
    unittest.main()
