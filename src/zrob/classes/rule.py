import logging
import pprint
import regex as re

from typing import Self, Any

from .. import colour as c
from .action import Action


log = logging.getLogger('zrob')


class Rule:
    def __init__(self, match: str):
        self.regex = re.compile(match)
        self.target: str = None
        self.prerequisites: dict[str, Any] = {}
        self.optionals: dict[str, Any] = {}
        self.actions: list[Action] = []

    def add_action(self, *actions) -> Self:
        self.actions += actions
        return self

    def requires(self, **kwargs: str) -> Self:
        """
        Add a mapping of requirements for this Target
        """
        self.prerequisites = kwargs
        return self

    def optional(self, **kwargs: str) -> Self:
        """
        Add a mapping of optional requirements for this Target
        """
        self.optionals = kwargs
        return self

    def prepare(self, target: str):
        self.tokens = self.match(target).groupdict()

        log.info(f"Materializing the rule {c.rule(self)} with {c.name(self.tokens)}")
        self.prerequisites = {
            name: kwarg.format(**self.tokens)
            for name, kwarg in self.prerequisites.items()
        } | {
            name: kwarg.format(**self.tokens)
            for name, kwarg in self.optionals.items()
        }

        log.info(f"Finished a list of prerequisites: {c.prereq(pprint.pformat(self.prerequisites, indent=4))}")

    def match(self, query):
        return self.regex.match(query)

    def __str__(self):
        return f"{self.regex.pattern!s}"

    def build(self):
        ok = True
        for action in self.actions:
            action.construct(self.prerequisites, self.target, **self.tokens)
            ok &= action.do()

        return ok

