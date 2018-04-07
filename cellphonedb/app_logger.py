import logging

import sys

app_logger = logging.getLogger(__name__)

if not app_logger.handlers:
    app_logger.propagate = False
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[+][APP][%(asctime)s][%(levelname)s] %(message)s', "%d/%m/%y-%H:%M:%S")
    ch.setFormatter(formatter)

    # TODO: Configurable logging level
    logging.basicConfig(level=logging.INFO)
    app_logger.addHandler(ch)
