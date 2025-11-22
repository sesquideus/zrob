import argparse
import logging

from typing import Optional as Opt

from .rule import Rule
from .. import colour as c

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('zrob')


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

    def build(self, what: Opt[str] = None):
        for target in self.targets:
            log.debug(f"Now trying to match a rule to {c.path(target)}")
            for rule in self.rules:
                if rule.match(target):
                    rule.target = target
                    log.debug(f"Matched rule {c.rule(rule)} with target {c.path(target)}")
                    rule.prepare(target)
                    rule.build()
                    return
            log.error(f"{c.err("No rule matched")} {c.path(target)}")
