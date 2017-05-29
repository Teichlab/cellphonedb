def get_column_table_names(model, db):
    colum_names = db.session.query(model).statement.columns
    colum_names = [p.name for p in colum_names]
    return colum_names