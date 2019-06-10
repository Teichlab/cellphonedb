class MissingR(Exception):
    def __init__(self):
        super().__init__('Missing R setup in current system')
