from .administration import AdministrationAgent
from .commercial import CommercialAgent
from .communication import CommunicationAgent
from .juridique import JuridiqueAgent
from .rh import RHAgent

AGENTS = {
    cls.key: cls
    for cls in (RHAgent, AdministrationAgent, CommercialAgent, CommunicationAgent, JuridiqueAgent)
}

__all__ = ["AGENTS", "RHAgent", "AdministrationAgent", "CommercialAgent", "CommunicationAgent", "JuridiqueAgent"]
