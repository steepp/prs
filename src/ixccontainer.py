from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone


@dataclass
class IxcContainer:
    name: str
    cpu_usage: int = field(default=0)
    memory_usage: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)
    status: str = ""
    ip_addresses: list = field(default_factory=list)

    def __post_init__(self):
        self.created_at = datetime.fromisoformat(self.created_at).astimezone(
            timezone.utc
        )
        if self.cpu_usage is None:
            self.cpu_usage = 0
        if self.memory_usage is None:
            self.memory_usage = 0
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.status is None:
            self.status = ""
        if self.ip_addresses is None:
            self.ip_addresses = []

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()
