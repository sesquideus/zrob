import logging

from .prereq import Prereq, Output, Optional

from .. import colour as c

log = logging.getLogger('zrob')


class Action:
    def __init__(self, *args: str | Prereq):
        self.args = list(args)
        log.debug(f"New action: {self}")

    def construct(self, prerequisites: dict[str, str], target, **args) -> str:
        log.debug(f"Constructing action: {c.act(self)} with prerequisites {c.prereq(prerequisites)} tokens {c.name(args)}")

        expanded = []
        for arg in self.args:
            if isinstance(arg, Prereq):
                expanded.append(prerequisites.get(arg.value))
            elif arg == Output:
                expanded.append(target)
            elif isinstance(arg, str):
                expanded.append(arg)
            elif isinstance(arg, Optional):
                expanded.append(arg.expand(prerequisites))
            else:
                raise TypeError(f"Unknown argument type: {arg}")

        log.debug(f"Constructed action: {' '.join(expanded)}")

    def __str__(self) -> str:
        return f"{' '.join(map(str, self.args))}"

    def do(self):
        log.debug(f"Doing action: {self}")


class CommandAction(Action):
    """
    An Action whose ultimate goal is to run a OS command
    """
    def do(self, dry_run: bool = True) -> None:
        pass

