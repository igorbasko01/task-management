from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    HIGH = 0
    MEDIUM = 1
    LOW = 2

    @property
    def display_name(self):
        return self.name.capitalize()

@dataclass
class TaskPriority:
    level: PriorityLevel

    @property
    def name(self) -> str:
        return self.level.display_name
    
    @property
    def numeric_value(self) -> int:
        return self.level.value

    @classmethod
    def from_numeric_value(cls, value: int):
        try:
            priority_level = PriorityLevel(value)
            return cls(level=priority_level)
        except ValueError:
            raise ValueError(f"Invalid priority value: {value}")
    
    @classmethod
    def from_name(cls, name: str):
        try:
            priority_level = PriorityLevel[name.upper()]
            return cls(level=priority_level)
        except KeyError:
            raise ValueError(f"Invalid priority name: {name}")