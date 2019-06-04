class PlotException(Exception):
    def __init__(self, msg):
        super().__init__('R Plot  Exception: {}'.format(msg))
