import pathlib
from typing import Callable


class Prereq:
    """
    Encapsulation of a prerequisite
    """
    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"




class Optional:
    def __init__(self, condition: Callable[[], bool], *args):
        self.condition = condition
        self.args = list(args)

    def expand(self, prerequisites: dict[str, str]) -> str:
        expanded = []
        for arg in self.args:
            if isinstance(arg, Prereq):
                expanded.append(prerequisites.get(arg.value))
            elif isinstance(arg, str):
                expanded.append(arg)
            else:
                raise TypeError(f"Unknown argument type: {arg}")
        return ' '.join(expanded)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.condition} => {self.args})"


class Output:
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name
