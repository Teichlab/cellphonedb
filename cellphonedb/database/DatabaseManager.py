class DatabaseManager:
    def __init__(self, repositories, db=None):
        self._repositories = repositories
        self.database = db

    # TODO: Throw error
    def add_repository(self, repository):
        if not self._repositories:
            self._repositories = {}

        self._repositories[repository.name] = repository

    def get_repository(self, respository_name):
        return self._repositories[respository_name](self)

    def get_column_table_names(self, model_name: str) -> object:
        def get_model():
            for c in self.database.base_model._decl_class_registry.values():
                if hasattr(c, '__tablename__') and c.__tablename__ == model_name:
                    return c

        colum_names = self.database.session.query(get_model()).statement.columns
        colum_names = [p.name for p in colum_names]
        return colum_names
