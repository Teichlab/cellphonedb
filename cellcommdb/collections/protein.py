import os
import pandas as pd
import numpy as np

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Multidata, Protein


def _get_column_table_names(model):
    colum_names = db.session.query(model).statement.columns
    return colum_names


def _remove_not_defined_columns(data_frame, defined_columns):
    data_frame_keys = data_frame.keys()

    for key in data_frame_keys:
        if key not in defined_columns:
            data_frame.drop(key, axis=1, inplace=True)

    return data_frame


def _get_existent_proteines(df_proteine):
    db_multidata = pd.read_sql_table(table_name='multidata', con=db.engine)
    csv_uniprots = df_proteine['uniprot'].tolist()

    db_multidata = db_multidata[db_multidata['uniprot'].apply(
        lambda x: x in csv_uniprots)]

    return db_multidata


def _save_proteins_in_db(unique_prots):
    _save_new_proteines(unique_prots)
    _update_proteine_multidata_in_db(unique_prots)


def _update_proteine_multidata_in_db(unique_prots):
    existent_uniprots = unique_prots[unique_prots['id'].notnull()]
    for index, unique_prot in existent_uniprots.iterrows():

        multidata = db.session.query(Multidata).get(unique_prot['id'])
        for key, value in unique_prot.to_dict().iteritems():

            if pd.isnull(value):
                setattr(multidata, key, None)
            else:
                setattr(multidata, key, value)

            db.session.commit()


def _insert_proteins_in_db(new_prots):
    for index, new_prot in new_prots.iterrows():
        protein = Protein()
        multidata = db.session.query(Multidata).filter_by(uniprot=new_prot['uniprot']).first()
        protein.multidata_id = multidata.id
        db.session.add(protein)
        db.session.commit()


def _save_new_proteines(unique_prots):
    new_uniprots = unique_prots[unique_prots['id'].isnull()]

    multi_adata_columns = _get_column_table_names(Multidata)
    new_uniprots = _remove_not_defined_columns(new_uniprots, multi_adata_columns)
    new_uniprots.drop('id', axis=1, inplace=True)

    new_uniprots.to_sql(name='multidata', if_exists='append', con=db.engine, index=False)
    _insert_proteins_in_db(new_uniprots)


def load(protein_file=None):
    bools = ['transmembrane', 'secretion', 'peripheral', 'receptor',
             'receptor_highlight', 'adhesion', 'other', 'transporter',
             'secreted_highlight']

    if not protein_file:
        protein_file = os.path.join(current_dir, 'data', 'protein.csv')

    csv_proteines_df = pd.read_csv(protein_file)

    csv_proteines_df['id'] = csv_proteines_df['id'].apply(lambda x: np.nan)

    csv_proteines_df[bools] = csv_proteines_df[bools].astype(bool)

    db_repeat_proteines_df = _get_existent_proteines(csv_proteines_df)

    all_prot_df = csv_proteines_df.append(db_repeat_proteines_df)

    unique_prots = _merge_same_proteines(all_prot_df, bools)

    _save_proteins_in_db(unique_prots)


def _merge_same_proteines(all_prot_df, bools):
    unique_prots = all_prot_df.drop_duplicates(subset=['uniprot'])

    def merge_values(row):
        proteine = all_prot_df[all_prot_df['uniprot'] == row['uniprot']]

        def setNonEmptyStrings(protRow):
            row[protRow.notnull()] = protRow[protRow.notnull()]

        proteine.apply(
            setNonEmptyStrings, axis=1
        )

        row[bools] = proteine[bools].any()

        return row

    unique_prots = unique_prots.apply(

        merge_values, axis=1
    )

    return unique_prots
