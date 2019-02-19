from enum import Enum

class AnalogicOperator(Enum):
    LESS_THAN = '<'
    MORE_THAN = '>'

    def __str__(self) -> str:
        return self.value
