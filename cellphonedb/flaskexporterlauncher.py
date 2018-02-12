from cellphonedb.api import output_dir
from cellphonedb.extensions import cellphonedb_flask
import inspect


class FlaskExporterLauncher(object):

    @staticmethod
    def all():
        # FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.protein)
        FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.complex)
        # FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.gene)
        # FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.interaction)

    @staticmethod
    def _call_cellphonecore_method(export_method, output_name=None, output_path=None):

        if not output_name:
            output_name = '%s.csv' % export_method.__name__

        if not output_path:
            output_path = output_dir

        result = export_method()
        result.to_csv('{}/{}'.format(output_path, output_name), index=False)

    def __getattr__(cls, method_name):
        def wrapper(output_name=None, output_path=None):
            export_method = getattr(cellphonedb_flask.cellphonedb.export, method_name)
            cls._call_cellphonecore_method(export_method, output_name, output_path)

        return wrapper

    # def gene(self, output_name=None):
    #     if not output_name:
    #         current_method_name = inspect.getframeinfo(inspect.currentframe()).function
    #         output_name = '%s.csv' % current_method_name
    #
    #     gene_query = db.session.query(Gene, Multidata.name).join(Protein).join(Multidata)
    #     gene_df = pd.read_sql(gene_query.statement, db.engine)
    #
    #     filters.remove_not_defined_columns(gene_df, database.get_column_table_names(Gene, db) + ['name'])
    #
    #     gene_df.drop(['id_gene', 'protein_id'], axis=1, inplace=True)
    #
    #     gene_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    #
    #     gene_df.to_csv('out/%s' % output_name, index=False)
