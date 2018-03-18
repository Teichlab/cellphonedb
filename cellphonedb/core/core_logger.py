import logging

import sys

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[+] [%(asctime)s] [%(levelname)s] %(message)s', "%d-%m-%y - %H:%M:%S")
ch.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG)
core_logger = logging.getLogger(__name__)
core_logger.addHandler(ch)
