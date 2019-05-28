class RRuntimeException(Exception):
    def __init__(self, msg):
        super().__init__('R Runtime Exception: {}'.format(msg))