import pandas as pd

from cellphonedb.extensions import db
from cellphonedb.models.complex.db_model_complex import Complex
from cellphonedb.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellphonedb.models.multidata.db_model_multidata import Multidata
from cellphonedb.models.protein.db_model_protein import Protein
from utilities import dataframe_format


def call():
    complex_query = db.session.query(Complex)
    multidata_query = db.session.query(Multidata)
    complex_composition_query = db.session.query(ComplexComposition)
    protein_query = db.session.query(Protein, Multidata).join(Multidata)

    complex_df = pd.read_sql(complex_query.statement, db.engine)
    multidata_df = pd.read_sql(multidata_query.statement, db.engine)
    complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)
    protein_df = pd.read_sql(protein_query.statement, db.engine)

    complex_complete = pd.merge(complex_df, multidata_df, left_on='complex_multidata_id',
                                right_on='id_multidata')

    composition = []
    for complex_index, complex in complex_df.iterrows():
        complex_complex_composition = complex_composition_df[
            complex_composition_df['complex_multidata_id'] == complex['complex_multidata_id']]

        protein_index = 1
        complex_proteins = {'complex_multidata_id': complex['complex_multidata_id'],
                            'uniprot_1': None, 'protein_1_gene_name': None,
                            'uniprot_2': None, 'protein_2_gene_name': None,
                            'uniprot_3': None, 'protein_3_gene_name': None,
                            'uniprot_4': None, 'protein_4_gene_name': None
                            }
        for index, complex_composition in complex_complex_composition.iterrows():
            proteine_name = \
                multidata_df[multidata_df['id_multidata'] == complex_composition['protein_multidata_id']][
                    'name'].values[0]
            complex_proteins['uniprot_%i' % protein_index] = proteine_name

            entry_name = protein_df[protein_df['name'] == proteine_name]['entry_name'].values[0]
            complex_proteins['protein_%i_gene_name' % protein_index] = entry_name
            protein_index += 1

        composition.append(complex_proteins)

    complex_complete = pd.merge(complex_complete, pd.DataFrame(composition), on='complex_multidata_id')
    complex_complete.drop(['id_multidata', 'id_complex', 'complex_multidata_id'], axis=1, inplace=True)

    # Edit order of the columns
    protein_headers = []

    for i in range(4):
        protein_headers.append('uniprot_%s' % (i + 1))
        protein_headers.append('protein_%s_gene_name' % (i + 1))

    complex_complete = dataframe_format.bring_columns_to_start(['name'] + protein_headers, complex_complete)
    complex_complete = dataframe_format.bring_columns_to_end(
        ['pdb_structure', 'pdb_id', 'stoichiometry', 'comments'], complex_complete)

    return complex_complete
