import os
import pandas as pd

from cellcommdb.api import current_dir
from cellcommdb.extensions import db
from cellcommdb.models.multidata.db_model_multidata import Multidata
from cellcommdb.models.multidata import properties_multidata
from cellcommdb.models.protein.db_model_protein import Protein
from cellcommdb.tools import filters, database


def load(protein_file=None):
    bools = ['transmembrane', 'secretion', 'peripheral', 'receptor',
             'receptor_highlight', 'adhesion', 'other', 'transporter',
             'secreted_highlight', 'iuhpar_ligand', 'cytoplasm', 'extracellular']

    if not protein_file:
        protein_file = os.path.join(current_dir, 'data', 'protein.csv')

    csv_proteins_df = pd.read_csv(protein_file)

    csv_proteins_df[bools] = csv_proteins_df[bools].astype(bool)

    proteins = _optimizations(csv_proteins_df)
    insert_multidata_proteins(proteins)
    insert_proteins_in_db(proteins)


def _optimizations(proteins):
    proteins['is_complex'] = False
    proteins['is_cellphone_receptor'] = proteins.apply(lambda protein: properties_multidata.is_receptor(protein),
                                                       axis=1)
    proteins['is_cellphone_ligand'] = proteins.apply(lambda protein: properties_multidata.is_ligand(protein), axis=1)

    return proteins


def insert_multidata_proteins(proteins):
    multidata_columns = database.get_column_table_names(Multidata, db)
    multidata_proteins = proteins.copy()
    multidata_proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)
    multidata_proteins = filters.remove_not_defined_columns(multidata_proteins, multidata_columns)
    multidata_proteins.to_sql(name='multidata', if_exists='append', con=db.engine, index=False)


def insert_proteins_in_db(proteins_df):
    multidatas = pd.read_sql_table(table_name='multidata', con=db.engine)
    multidatas.rename(index=str, columns={'id_multidata': 'protein_multidata_id'}, inplace=True)
    proteins = proteins_df.copy()
    proteins.rename(index=str, columns={'uniprot': 'name'}, inplace=True)

    proteins = pd.merge(proteins, multidatas, on='name')

    proteins = filters.remove_not_defined_columns(proteins, database.get_column_table_names(Protein, db))
    proteins.to_sql(name='protein', if_exists='append', con=db.engine, index=False)
