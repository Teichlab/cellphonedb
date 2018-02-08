class DatabaseManager:
    def __init__(self, repositories, db=None):
        self._repositories = repositories
        self.database = db

    def add_repository(self, repository):
        if not self._repositories:
            self._repositories = {}

        self._repositories[repository.name] = repository

    def get_repository(self, respository_name):
        return self._repositories[respository_name]
