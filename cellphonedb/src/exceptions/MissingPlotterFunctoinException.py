class MissingPlotterFunctionException(Exception):
    def __init__(self):
        super().__init__('Selected plotter function not available')