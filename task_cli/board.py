from dataclasses import dataclass


@dataclass
class Board:
    name: str
    acronym: str

    @classmethod
    def from_allowed_boards(cls, board_name: str, allowed_boards: list):
        for board in allowed_boards:
            if board == board_name:
                return board
        raise ValueError(f"Invalid board: {board_name}")

    def __eq__(self, other):
        other_name = ""
        other_acronym = ""
        
        if not other:
            return False
        
        if isinstance(other, Board):
            other_name = other.name
            other_acronym = other.acronym
        
        if isinstance(other, str):
            other_name = other
            other_acronym = other

        return self.name.lower() == other_name.lower() or self.acronym.lower() == other_acronym.lower()
    
    def __str__(self):
        return f"{self.name} ({self.acronym})"