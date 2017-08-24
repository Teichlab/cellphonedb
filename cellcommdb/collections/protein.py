import os
import pandas as pd
import numpy as np

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models import Multidata, Protein
from cellcommdb.tools import filters, database


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

    unique_prots['membrane_type'] = None
    _defineProteinType(unique_prots, 'Single-pass+type+I.csv', 'singlepass_typeI')
    _defineProteinType(unique_prots, 'Single-pass+type+II.csv', 'singlepass_typeII')
    _defineProteinType(unique_prots, 'Single-pass+type+III.csv', 'singlepass_typeIII')
    _defineProteinType(unique_prots, 'Single-pass+type+IV.csv', 'singlepass_typeIV')
    _defineProteinType(unique_prots, 'Multi-pass.csv', 'multipass')
    _defineProteinType(unique_prots, 'GPI-anchor.csv', 'GPI-anchor')

    _save_proteins_in_db(unique_prots)



def _defineProteinType(proteins_df, protein_type_file, type_name):
    protein_type_file = os.path.join(current_dir, 'data', protein_type_file)
    proteins_type_x = pd.read_csv(protein_type_file, sep=';')['Entry'].tolist()

    proteins_df['membrane_type'][proteins_df.apply(
        lambda x: x['uniprot'] in proteins_type_x, axis=1)] = type_name


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
        for key, value in unique_prot.to_dict().items():

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

    proteins = filters.remove_not_defined_columns(proteins, database.get_column_table_names(Protein, db))

    proteins.drop('id', axis=1, inplace=True)

    proteins.to_sql(name='protein', if_exists='append', con=db.engine, index=False)


def _insert_multidata_proteins(proteins):
    multidata_columns = database.get_column_table_names(Multidata, db)
    multidata_proteins = proteins.copy()
    multidata_proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)
    multidata_proteins = filters.remove_not_defined_columns(multidata_proteins, multidata_columns)
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
