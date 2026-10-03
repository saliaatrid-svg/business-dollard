from .administration import AdministrationAgent
from .commercial import CommercialAgent
from .communication import CommunicationAgent
from .juridique import JuridiqueAgent
from .rh import RHAgent
from .strategie import StrategieAgent

AGENTS = {
    cls.key: cls
    for cls in (
        RHAgent,
        AdministrationAgent,
        CommercialAgent,
        CommunicationAgent,
        JuridiqueAgent,
        StrategieAgent,
    )
}

__all__ = ["AGENTS", "RHAgent", "AdministrationAgent", "CommercialAgent", "CommunicationAgent", "JuridiqueAgent", "StrategieAgent"]
