import logging


class LogLevels(logging.Filter):
    def __init__(self, levels=None):
        super(LogLevels, self).__init__()
        self._levels = levels

    def filter(self, record):
        if record.levelname in self._levels:
            return True
        return False