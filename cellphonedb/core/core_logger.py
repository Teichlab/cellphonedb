import logging

import sys

core_logger = logging.getLogger(__name__)

if not core_logger.handlers:
    core_logger.propagate = False
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[+][CORE][%(asctime)s][%(levelname)s] %(message)s', "%d/%m/%y-%H:%M:%S")
    ch.setFormatter(formatter)

    # TODO: Configurable logging level
    logging.basicConfig(level=logging.WARNING)
    core_logger.addHandler(ch)
