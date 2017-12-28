import os
import pandas as pd

from cellphonedb.api import current_dir
from cellphonedb.extensions import db
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.multidata import properties_multidata
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein
from cellphonedb.tools import filters, database


def load(complex_file=None):
    """
    Uploads complex data from csv.

    - Creates new complexes in Multidata table
    - Creates reference in Complex table
    - Creates complex composition to define complexes.
    :param complex_file:
    :return:
    """
    if not complex_file:
        complex_file = os.path.join(current_dir, 'data', 'complex.csv')

    existing_complexes = db.session.query(Multidata.name).all()
    existing_complexes = [c[0] for c in existing_complexes]
    proteins = db.session.query(Multidata.name, Multidata.id_multidata).join(Protein).all()
    proteins = {p[0]: p[1] for p in proteins}
    # Read in complexes
    complex_df = pd.read_csv(complex_file, quotechar='"', na_values="NA", sep=',')
    complex_df.dropna(axis=1, inplace=True, how='all')
    complex_df.rename(index=str, columns={'complex_name': 'name'}, inplace=True)

    # Get complex composition info
    complete_indices = []
    incomplete_indices = []
    missing_proteins = []
    complex_map = {}
    for index, row in complex_df.iterrows():
        missing = False
        protein_id_list = []
        for protein in ['protein_1', 'protein_2',
                        'protein_3', 'protein_4']:
            if not pd.isnull(row[protein]):
                protein_id = proteins.get(row[protein])
                if protein_id is None:
                    missing = True
                    missing_proteins.append(row[protein])
                else:
                    protein_id_list.append(protein_id)
        if not missing:
            complex_map[row['name']] = protein_id_list
            complete_indices.append(int(index))
        else:
            incomplete_indices.append(index)

    if len(incomplete_indices) > 0:
        print('MISSING PROTEINS:')
        for protein in missing_proteins:
            print(protein)

        print('COMEPLEXES WITH MISSING PROTEINS:')
        print(complex_df.iloc[incomplete_indices, :]['name'])

    # Insert complexes
    if not complex_df.empty:
        # Remove unwanted columns
        removal_columns = list([x for x in complex_df.columns if 'protein_' in x or 'Name_' in x or 'Unnamed' in x])
        # removal_columns += ['comments']
        complex_df.drop(removal_columns, axis=1, inplace=True)

        # Remove rows with missing complexes
        complex_df = complex_df.iloc[complete_indices, :]

        # Convert ints to bool
        bools = ['receptor', 'receptor_highlight', 'adhesion', 'other',
                 'transporter', 'secreted_highlight', 'transmembrane', 'secretion', 'peripheral', 'iuhpar_ligand',
                 'extracellular', 'cytoplasm']
        complex_df[bools] = complex_df[bools].astype(bool)

        # Drop existing complexes
        complex_df = complex_df[complex_df['name'].apply(
            lambda x: x not in existing_complexes)]

        multidata_df = filters.remove_not_defined_columns(complex_df.copy(),
                                                          database.get_column_table_names(Multidata, db))

        multidata_df = _optimitzations(multidata_df)
        multidata_df.to_sql(name='multidata', if_exists='append', con=db.engine, index=False)

    # Now find id's of new complex rows
    new_complexes = db.session.query(Multidata.name, Multidata.id_multidata).all()
    new_complexes = {c[0]: c[1] for c in new_complexes}

    # Build set of complexes
    complex_set = []
    complex_table = []
    for complex_name in complex_map:
        complex_id = new_complexes[complex_name]
        for protein_id in complex_map[complex_name]:
            complex_set.append((complex_id, protein_id, len(complex_map[complex_name])))
        complex_table.append({'complex_multidata_id': complex_id, 'name': complex_name})

    # Insert complex composition
    complex_set_df = pd.DataFrame(complex_set,
                                  columns=['complex_multidata_id', 'protein_multidata_id', 'total_protein'])

    complex_table_df = pd.DataFrame(complex_table)
    complex_table_df = pd.merge(complex_table_df, complex_df, on='name')

    filters.remove_not_defined_columns(complex_table_df, database.get_column_table_names(Complex, db))

    complex_table_df.to_sql(
        name='complex', if_exists='append',
        con=db.engine, index=False)

    complex_set_df.to_sql(
        name='complex_composition', if_exists='append',
        con=db.engine, index=False)


def _optimitzations(multidata):
    multidata['is_complex'] = True
    multidata['is_cellphone_receptor'] = multidata.apply(lambda protein: properties_multidata.is_receptor(protein),
                                                         axis=1)
    multidata['is_cellphone_ligand'] = multidata.apply(lambda protein: properties_multidata.is_ligand(protein), axis=1)

    return multidata
