from cellphonedb.extensions import cellphonedb_flask
from cellphonedb.flask_app import output_dir


class FlaskTerminalOptimizerLauncher():
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
            export_method = getattr(cellphonedb_flask.cellphonedb.optimizer, method_name)
            cls._call_cellphonecore_method(export_method, output_name, output_path)

        return wrapper
