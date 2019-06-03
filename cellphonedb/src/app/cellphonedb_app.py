import os

from cellphonedb.src.app.flask.flask_cellphonedb import CellphonedbFlask

cellphonedb_app = CellphonedbFlask()

file_current_dir = os.path.dirname(os.path.realpath(__file__))
current_execution_dir = os.getcwd()

core_dir = '%s/../core' % file_current_dir
data_dir = '%s/data' % core_dir
output_dir = '%s/out' % current_execution_dir
query_input_dir = '%s' % current_execution_dir
temp_dir = '%s/../../temp' % file_current_dir
output_test_dir = '{}/../tests/out'.format(file_current_dir)
data_test_dir = '{}/../tests/fixtures'.format(file_current_dir)
