from enum import Enum

class SIGNAL(Enum):
    LOW = 'LOW'
    HIGH = 'HIGH'

    def __str__(self) -> str:
        return self.value