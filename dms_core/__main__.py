import argparse

from . import Memory, Orchestrator
from .agents import AGENTS


def main():
    parser = argparse.ArgumentParser(prog="python -m dms_core", description="Agents IA de DMS")
    parser.add_argument("demande", help="La demande, entre guillemets")
    parser.add_argument("--agent", choices=sorted(AGENTS), help="Forcer un agent (sinon choix automatique)")
    parser.add_argument("--note", help="Ajouter une note à la mémoire (sans donnée de santé)")
    args = parser.parse_args()

    memory = Memory()
    if args.note:
        memory.add_note(args.note, agent=args.agent or "")
    orchestrator = Orchestrator(memory)
    key, output = orchestrator.handle(args.demande, agent=args.agent)
    if key:
        print(f"[{orchestrator.prenom} a confié la demande à : {orchestrator.agents[key].prenom} ({key})]\n")
    print(output)


if __name__ == "__main__":
    main()
