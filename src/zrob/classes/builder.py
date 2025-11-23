import argparse
import logging
from pathlib import Path

from typing import Optional as Opt

from .rule import Rule
from .. import colour as c
from .. import logger

log = logger.setup_log('zrob')


class Builder:
    """
    The main class of zrob. Explicit af.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('targets', type=str, nargs='+')
        self.parser.add_argument('--debug', action='store_true')

        args = self.parser.parse_args()

        if args.debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        self.rules = set()
        self.targets = set(args.targets)

    def register(self, target: Rule):
        self.rules.add(target)

    def go(self):
        for target in self.targets:
            if (result := self.build(target)) == True:
                log.info(f"Build {c.ok('succeeded')} for {c.path(target)}")
            else:
                log.error(f"Build failed for {c.path(target)}")

    def build(self, what: Opt[str] = None):
        log.debug(f"Now trying to match a rule to {c.path(what)}")

        for rule in self.rules:
            if rule.match(what):
                rule.target = what
                log.debug(f"Matched rule {c.rule(rule)} for target {c.path(what)}")
                rule.prepare(what)

                fulfilled = True

                for name, path in rule.prerequisites.items():
                    log.debug(f"Prerequisite {c.prereq(path)}")
                    fulfilled &= self.build(path)

                if fulfilled:
                    log.debug(f"All prerequisited have been met")
                    return rule.build()
                else:
                    return False

        log.info(f"{c.err("No rule can process")} {c.path(what)}")

        if Path(what).exists():
            log.debug(f"Object {c.path(what)} exists in the filesystem")
            return True
        else:
            log.critical(f"Object {c.path(what)} does not exist and does not match any rules. Cannot continue.")
            return False