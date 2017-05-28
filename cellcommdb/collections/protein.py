import os
import pandas as pd
import numpy as np

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Multidata, Protein


def load(protein_file=None):
    bools = ['transmembrane', 'secretion', 'peripheral', 'receptor',
             'receptor_highlight', 'adhesion', 'other', 'transporter',
             'secreted_highlight']

    if not protein_file:
        protein_file = os.path.join(current_dir, 'data', 'protein.csv')

    csv_proteins_df = pd.read_csv(protein_file)

    _clear_column(csv_proteins_df, 'id')

    csv_proteins_df[bools] = csv_proteins_df[bools].astype(bool)

    db_repeat_proteins_df = _get_existent_proteins(csv_proteins_df)
    db_repeat_proteins_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

    all_prot_df = csv_proteins_df.append(db_repeat_proteins_df)

    unique_prots = _merge_same_proteins(all_prot_df, bools)

    _save_proteins_in_db(unique_prots)


def _get_column_table_names(model):
    colum_names = db.session.query(model).statement.columns
    colum_names = [p.name for p in colum_names]
    return colum_names


def _remove_not_defined_columns(data_frame, defined_columns):
    data_frame_keys = data_frame.keys()

    for key in data_frame_keys:
        if key not in defined_columns:
            data_frame.drop(key, axis=1, inplace=True)

    return data_frame


def _get_existent_proteins(df_protein):
    db_multidata = pd.read_sql_table(table_name='multidata', con=db.engine)
    csv_uniprots = df_protein['uniprot'].tolist()
    db_multidata.rename(index=str, columns={'name': 'uniprot'}, inplace=True)
    db_multidata = db_multidata[db_multidata['uniprot'].apply(
        lambda x: x in csv_uniprots)]

    return db_multidata


def _save_proteins_in_db(unique_prots):
    _insert_new_proteins(unique_prots)
    _update_protein_multidata_in_db(unique_prots)


def _update_protein_multidata_in_db(unique_prots):
    existent_uniprots = unique_prots[unique_prots['id'].notnull()]
    for index, unique_prot in existent_uniprots.iterrows():

        multidata = db.session.query(Multidata).get(unique_prot['id'])
        for key, value in unique_prot.to_dict().iteritems():

            if pd.isnull(value):
                setattr(multidata, key, None)
            else:
                setattr(multidata, key, value)

            db.session.commit()


def _insert_proteins_in_db(proteins_df):
    multidatas = pd.read_sql_table(table_name='multidata', con=db.engine)
    multidatas.rename(index=str, columns={'id': 'protein_multidata_id'}, inplace=True)

    proteins = proteins_df.copy()
    proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)

    proteins = pd.merge(proteins, multidatas, on='name')
    proteins = _remove_not_defined_columns(proteins, _get_column_table_names(Protein))

    proteins.drop('id', axis=1, inplace=True)

    proteins.to_sql(name='protein', if_exists='append', con=db.engine, index=False)


def _insert_multidata_proteins(proteins):
    multidata_columns = _get_column_table_names(Multidata)
    multidata_proteins = proteins.copy()
    multidata_proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)
    multidata_proteins = _remove_not_defined_columns(multidata_proteins, multidata_columns)
    multidata_proteins.drop('id', axis=1, inplace=True)

    multidata_proteins.to_sql(name='multidata', if_exists='append', con=db.engine, index=False)


def _insert_new_proteins(unique_prots):
    new_uniprots = unique_prots[unique_prots['id'].isnull()]
    _insert_multidata_proteins(new_uniprots)
    _insert_proteins_in_db(new_uniprots)


def _clear_column(data_frame, column_name):
    data_frame[column_name] = data_frame[column_name].apply(lambda x: np.nan)


def _merge_same_proteins(all_prot_df, bools):
    unique_prots = all_prot_df.drop_duplicates(subset=['uniprot'])

    def merge_values(row):
        protein = all_prot_df[all_prot_df['uniprot'] == row['uniprot']]

        def setNonEmptyStrings(protRow):
            row[protRow.notnull()] = protRow[protRow.notnull()]

        protein.apply(
            setNonEmptyStrings, axis=1
        )

        row[bools] = protein[bools].any()

        return row

    unique_prots = unique_prots.apply(

        merge_values, axis=1
    )

    return unique_prots
