from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class IxcContainer:
    name: str
    cpu_usage: int
    memory_usage: int
    created_at: datetime
    status: str
    ip_addresses: list

    def __post_init__(self):
        self.created_at = datetime.fromisoformat(self.created_at).astimezone(
            timezone.utc
        )
