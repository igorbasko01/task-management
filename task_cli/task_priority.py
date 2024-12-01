from dataclasses import dataclass


@dataclass
class TaskPriority:
    name: str
    numeric_value: int  # Lower value means higher priority

    _value_map = {
        0: "High",
        1: "Medium",
        2: "Low"
    }

    @classmethod
    def from_numeric_value(cls, value: int):
        if value not in cls._value_map.keys():
            raise ValueError(f"Invalid priority value: {value}")
        name = cls._value_map[value]
        return cls(name=name, numeric_value=value)
    
    @classmethod
    def from_name(cls, name: str):
        for value, priority in cls._value_map.items():
            if priority == name:
                return cls(name=priority, numeric_value=value)
        raise ValueError(f"Invalid priority name: {name}")