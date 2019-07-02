import logging
import sys


class RabbitLogger:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        formatter = logging.Formatter('[ ][QUEUE][%(asctime)s][%(levelname)s] %(message)s', "%d/%m/%y-%H:%M:%S")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def __getattr__(self, item):
        return getattr(self._logger, item)


class RabbitAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[{}] {}'.format(self.extra['job_id'], msg), kwargs

    @classmethod
    def logger_for(cls, logger, job_id):
        return cls(logger, {'job_id': job_id})
