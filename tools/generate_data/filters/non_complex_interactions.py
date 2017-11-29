import os

import pandas as pd

from tools.app import data_dir, output_dir, current_dir


def only_noncomplex_interactions(inweb_namefile, complexes_namefile):
    if os.path.isfile('%s/%s' % (data_dir, inweb_namefile)):
        inweb_file = os.path.join(data_dir, inweb_namefile)
    else:
        inweb_file = os.path.join(output_dir, inweb_namefile)

    complexes_file = os.path.join(current_dir, 'data', complexes_namefile)

    complexes_df = pd.read_csv(complexes_file)

    proteins_in_complex = []

    for i in range(1, 5):
        proteins_in_complex = proteins_in_complex + complexes_df['protein_%s' % i].dropna().tolist()

    proteins_in_complex = list(set(proteins_in_complex))

    inweb_df = pd.read_csv(inweb_file)

    inweb_df_no_complex = inweb_df[inweb_df['protein_1'].apply(
        lambda protein: protein not in proteins_in_complex
    )]
    inweb_df_no_complex = inweb_df_no_complex[
        inweb_df_no_complex['protein_2'].apply(
            lambda protein: protein not in proteins_in_complex
        )]

    output_name = 'no_complex_interactions.csv'
    inweb_df_no_complex.to_csv('%s/out/%s' % (current_dir, output_name),
                               index=False, float_format='%.4f')
