import logging
import subprocess

from .prereq import Prereq, Output, Optional

from .. import colour as c

log = logging.getLogger('zrob')


class Action:
    def __init__(self, *args: str | Prereq):
        self.args = list(args)
        log.debug(f"New action: {c.act(self)}")

    def construct(self, prerequisites: dict[str, str], target, **args) -> str:
        log.debug(f"Constructing action: {c.act(self)} with prerequisites {c.prereq(prerequisites)} tokens {c.name(args)}")

        expanded = []
        for arg in self.args:
            if isinstance(arg, Prereq):
                try:
                    expanded.append(prerequisites[arg.value])
                except KeyError as e:
                    log.error(f"Unrecognized prerequisite {e}")
                    raise e
            elif arg == Output:
                expanded.append(target)
            elif isinstance(arg, str):
                expanded.append(arg)
            elif isinstance(arg, Optional):
                if arg.condition:
                    expanded.append(arg.expand(prerequisites))
            else:
                raise TypeError(f"Unknown argument type: {arg}")

        self.constructed = ' '.join(expanded)
        log.debug(f"Constructed action: {self.constructed}")

    def __str__(self) -> str:
        return f"{' '.join(map(str, self.args))}"

    def do(self, dry_run: bool = False) -> bool:
        if dry_run:
            log.debug(f"Pretending to do action: {c.act(self)}")
            return True
        else:
            log.debug(f"Doing action {c.act(self)}")
            return subprocess.run(self.constructed).returncode


class Command(Action):
    """
    An Action whose ultimate goal is to run a OS command
    """
    def do(self, dry_run: bool = True) -> bool:
        return super().do(dry_run=True)

