from cellcommdb.queries.query0 import Query0


class Queries(object):
    def __init__(self, app):
        self.app = app

    def query0(self):
        Query0.call()
