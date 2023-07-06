from dataclasses import dataclass

@dataclass
class SelectContainer():
    column_name: str
    path: str

@dataclass
class CreateContainer():
    type: str
    path: str

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def __le__(self, other):
        return self.path < self.other

    def __gt__(self, other):
        return self.path > other.path