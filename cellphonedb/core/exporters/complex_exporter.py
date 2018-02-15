import pandas as pd

from utilities import dataframe_format


def call(complexes, multidatas, complex_compositions, proteins):
    complex_complete = pd.merge(complexes, multidatas, left_on='complex_multidata_id',
                                right_on='id_multidata')

    composition = []
    for complex_index, complex in complexes.iterrows():
        complex_complex_composition = complex_compositions[
            complex_compositions['complex_multidata_id'] == complex['complex_multidata_id']]

        protein_index = 1
        complex_proteins = {'complex_multidata_id': complex['complex_multidata_id'],
                            'uniprot_1': None, 'protein_1_gene_name': None,
                            'uniprot_2': None, 'protein_2_gene_name': None,
                            'uniprot_3': None, 'protein_3_gene_name': None,
                            'uniprot_4': None, 'protein_4_gene_name': None
                            }
        for index, complex_composition in complex_complex_composition.iterrows():
            proteine_name = \
                multidatas[multidatas['id_multidata'] == complex_composition['protein_multidata_id']][
                    'name'].values[0]
            complex_proteins['uniprot_%i' % protein_index] = proteine_name

            entry_name = proteins[proteins['name'] == proteine_name]['entry_name'].values[0]
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
        ['pdb_structure', 'pdb_id', 'stoichiometry', 'comments_complex'], complex_complete)

    return complex_complete
