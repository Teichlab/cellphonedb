import os

from cellphonedb.app.flask.flask_cellphonedb import CellphonedbFlask

cellphonedb_app = CellphonedbFlask()

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = '%s/../core/data' % current_dir
output_dir = '%s/../../out' % current_dir
temp_dir = '%s/../../temp' % current_dir
query_input_dir = '%s/../../in' % current_dir
output_test_dir = '{}/../tests/out'.format(current_dir)
data_test_dir = '{}/../tests/fixtures'.format(current_dir)
