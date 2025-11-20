import subprocess


class Action:
    pass


class Target:
    def __init__(self, match: str):
        self.regex = re.compile(match)


    def build(self):
        pass

    def add_actions(self, primary, *args):
        self.actions.append(primary, *args)

    def build(self):
        subprocess.run(primary, *args)

    def match(self, query):
        return self.regex.match(query)



class Builder:
    """
    The main class of zrob. Explicit af.
    """
    def __init__(self):
        self.targets = set()

    def register(target: Target):
        self.targets.add(target)

    def build(self, what: Optional[str] = None):
        for target in self.targets:
            if target.match(what):
                target.build()
