import os

import pandas as pd

from tools.app import current_dir, output_dir
from tools.interaction_actions import _download_inwebinbiomap, _only_uniprots_in_df


def generate_interactions_inweb(inweb_inbiomap_namefile, database_proteins_namefile):
    if not inweb_inbiomap_namefile:
        inweb_inbiomap_namefile = _download_inwebinbiomap()
        inweb_inbiomap_file = os.path.join(inweb_inbiomap_namefile)
    else:
        inweb_inbiomap_file = os.path.join(current_dir, 'data', inweb_inbiomap_namefile)

    inweb_inbiomap_df = pd.read_csv(inweb_inbiomap_file, delimiter='\t', na_values='-')

    inweb_interactions = pd.DataFrame()

    inweb_interactions['protein_1'] = inweb_inbiomap_df.take([0], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['protein_2'] = inweb_inbiomap_df.take([1], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['score_1'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: 0 if protein.values[0].split('|')[0] == '-' else protein.values[0].split('|')[0], axis=1)
    inweb_interactions['score_2'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: 0 if protein.values[0].split('|')[1] == '-' else protein.values[0].split('|')[1], axis=1)

    inweb_interactions['source'] = 'inweb'

    database_proteins_file = os.path.join(current_dir, 'data', database_proteins_namefile)

    database_proteins_df = pd.read_csv(database_proteins_file)

    inweb_interactions = _only_uniprots_in_df(database_proteins_df, inweb_interactions)

    inweb_interactions.to_csv('%scellphone_interactions_inweb.csv' % output_dir, index=False)
