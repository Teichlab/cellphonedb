import os

import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Multidata, Interaction, Complex_composition
from cellcommdb.tools import filters, database


def load(interaction_file=None):
    if not interaction_file:
        interaction_file = os.path.join(current_dir, 'data', 'inweb_interaction.csv')

    csv_interaction_df = pd.read_csv(interaction_file, quotechar='"', na_values="-")

    multidata_query = db.session.query(Multidata.id, Multidata.name)
    multidata_df = pd.read_sql(multidata_query.statement, db.engine)

    interaction_df = pd.merge(csv_interaction_df, multidata_df, left_on='protein_uniprot_1_id', right_on='name')
    interaction_df.rename(index=str, columns={'id': 'unityinteraction_multidata_1_id'}, inplace=True)
    interaction_df = pd.merge(interaction_df, multidata_df, left_on='protein_uniprot_2_id', right_on='name')
    interaction_df.rename(index=str, columns={'id': 'unityinteraction_multidata_2_id'}, inplace=True)
    interaction_df.rename(index=str, columns={'score1': 'score_1'}, inplace=True)
    interaction_df.rename(index=str, columns={'score2': 'score_2'}, inplace=True)

    filters.remove_not_defined_columns(interaction_df, database.get_column_table_names(Interaction, db))

    if len(interaction_df) < len(csv_interaction_df):
        print 'SOME PROTEINS DIDNT EXISTS, PLEASE, CHECK IT'

    interaction_df_clean = remove_interaction_in_complex(interaction_df)



    interaction_df_clean.to_sql(name='interaction', if_exists='append', con=db.engine, index=False)


    # interactions = []
    # missing_proteins = []
    # incomplete_interactions_indices = []
    #
    # for index, interaction in csv_interaction_df.iterrows():
    #     incomplete = False
    #     unityinteraction_multidata_1 = multidata_df[multidata_df['name'] == interaction['protein_uniprot_1_id']]
    #     unityinteraction_multidata_2 = multidata_df[multidata_df['name'] == interaction['protein_uniprot_2_id']]
    #
    #     if (unityinteraction_multidata_1.empty):
    #         incomplete = True
    #         missing_proteins.append(interaction['protein_uniprot_1_id'])
    #
    #     if (unityinteraction_multidata_2.empty):
    #         incomplete = True
    #         missing_proteins.append(interaction['protein_uniprot_2_id'])
    #
    #     if incomplete:
    #         missing_proteins.append(index)
    #         continue
    #
    #     interactions.append({'unityinteraction_multidata_1_id': unityinteraction_multidata_1['id'],
    #                         'unityinteraction_multidata_2_id': unityinteraction_multidata_2['id'],
    #                         'score_1': interaction['score1'],
    #                         'score_2': interaction['score2']
    #                         })
    #
    # if missing_proteins:
    #     print 'MISSING PROTEINS:'
    #     for protein in missing_proteins:
    #         print protein
    #
    #
    # interactions_df = pd.DataFrame(interactions)
    #
    #
    # filters.remove_not_defined_columns(interactions_df, database.get_column_table_names(Interaction, db))
    #
    # print interactions_df
    # interactions_df.to_sql(name='interaction', if_exists='append', con=db.engine, index=False)


def remove_interaction_in_complex(interaction_df):
    complex_composition_query = db.session.query(Complex_composition.protein_multidata_id)
    complex_composition = pd.read_sql(complex_composition_query.statement, db.engine)[
        'protein_multidata_id'].tolist()
    interaction_df_clean = interaction_df[interaction_df['unityinteraction_multidata_1_id'].apply(
        lambda multidata_id: multidata_id not in complex_composition
    )]
    interaction_df_clean = interaction_df_clean[interaction_df_clean['unityinteraction_multidata_2_id'].apply(
        lambda multidata_id: multidata_id not in complex_composition
    )]
    return interaction_df_clean
