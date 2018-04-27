class BasePlugin:

    def __init__(self, args):
        self.args = args

    def execute(self, data):
        raise NotImplementedError
