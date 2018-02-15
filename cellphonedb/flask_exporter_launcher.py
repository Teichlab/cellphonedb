from cellphonedb.api import output_dir
from cellphonedb.extensions import cellphonedb_flask


class FlaskExporterLauncher(object):

    @staticmethod
    def all():
        FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.protein)
        FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.complex)
        FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.gene)
        FlaskExporterLauncher._call_cellphonecore_method(cellphonedb_flask.cellphonedb.export.interaction)

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
