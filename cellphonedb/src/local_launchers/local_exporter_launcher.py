from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import cellphonedb_app, output_dir


class LocalExporterLauncher(object):
    @staticmethod
    def all():
        LocalExporterLauncher._call_cellphonecore_method(cellphonedb_app.cellphonedb.export.protein)
        LocalExporterLauncher._call_cellphonecore_method(cellphonedb_app.cellphonedb.export.complex)
        LocalExporterLauncher._call_cellphonecore_method(cellphonedb_app.cellphonedb.export.gene)
        LocalExporterLauncher._call_cellphonecore_method(cellphonedb_app.cellphonedb.export.interaction)

    @staticmethod
    def _call_cellphonecore_method(export_method, output_name=None, output_path=None):
        app_logger.debug('Exporting {}'.format(export_method.__name__))
        if not output_name:
            output_name = '%s.csv' % export_method.__name__

        if not output_path:
            output_path = output_dir

        result = export_method()
        result.to_csv('{}/{}'.format(output_path, output_name), index=False)

    def __getattr__(cls, method_name):
        def wrapper(output_name=None, output_path=None):
            export_method = getattr(cellphonedb_app.cellphonedb.export, method_name)
            cls._call_cellphonecore_method(export_method, output_name, output_path)

        return wrapper
