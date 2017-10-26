import os

import pandas as pd

from tools.app import current_dir
from cellcommdb.tools.filters import remove_not_defined_columns


def only_noncomplex_interactions(complexes_namefile, inweb_namefile):
    complexes_file = os.path.join(current_dir, 'data', complexes_namefile)

    complexes_df = pd.read_csv(complexes_file)

    proteins_in_complex = []

    for i in range(1, 5):
        proteins_in_complex = proteins_in_complex + complexes_df['protein_%s' % i].dropna().tolist()

    proteins_in_complex = list(set(proteins_in_complex))

    inweb_file = os.path.join(current_dir, 'data', inweb_namefile)

    inweb_df = pd.read_csv(inweb_file)

    inweb_df_no_complex = inweb_df[inweb_df['protein_1'].apply(
        lambda protein: protein not in proteins_in_complex
    )]
    inweb_df_no_complex = inweb_df_no_complex[
        inweb_df_no_complex['protein_2'].apply(
            lambda protein: protein not in proteins_in_complex
        )]

    output_name = 'inweb_interactions_no_complex.csv'
    inweb_df_no_complex.to_csv('%s/out/%s' % (current_dir, output_name), index=False)

    print(inweb_df_no_complex)


def generate_inweb_interactions(database_proteins_namefile, inweb_inbiomap_namefile=None):
    # TODO: Download inweb_inbiomap
    inweb_inbiomap_file = None
    if inweb_inbiomap_namefile:
        inweb_inbiomap_file = os.path.join(current_dir, 'data', inweb_inbiomap_namefile)

    inweb_inbiomap_df = pd.read_csv(inweb_inbiomap_file, delimiter='\t')

    inweb_interactions = pd.DataFrame()

    inweb_interactions['protein_1'] = inweb_inbiomap_df.take([0], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['protein_2'] = inweb_inbiomap_df.take([1], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['score_1'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: protein.values[0].split('|')[0], axis=1)
    inweb_interactions['score_2'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: protein.values[0].split('|')[1], axis=1)

    database_proteins_file = os.path.join(current_dir, 'data', database_proteins_namefile)

    database_proteins_df = pd.read_csv(database_proteins_file)

    inweb_interactions = _only_uniprots_in_df(database_proteins_df, inweb_interactions)

    output_name = 'cellphone_inweb.csv'

    inweb_interactions.to_csv('%s/out/%s' % (current_dir, output_name), index=False)


def _only_uniprots_in_df(uniprots_df, inweb_interactions):
    inweb_cellphone = pd.merge(inweb_interactions, uniprots_df, left_on=['protein_1'],
                               right_on=['uniprot'], how='inner')

    inweb_cellphone = pd.merge(inweb_cellphone, uniprots_df, left_on=['protein_2'],
                               right_on=['uniprot'], how='inner')

    return remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)
