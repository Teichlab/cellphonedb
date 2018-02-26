import pandas as pd

from utils import dataframe_format


# TODO: Move to helper
def call(complexes: pd.DataFrame, multidatas: pd.DataFrame, complex_compositions: pd.DataFrame,
         proteins: pd.DataFrame) -> pd.DataFrame:
    complex_complete = pd.merge(complexes, multidatas, left_on='complex_multidata_id',
                                right_on='id_multidata')

    composition = []
    for complex_index, complex in complexes.iterrows():
        complex_complex_composition = complex_compositions[
            complex_compositions['complex_multidata_id'] == complex['complex_multidata_id']]

        protein_index = 1
        complex_proteins = {
            'complex_multidata_id': complex['complex_multidata_id'],
            'uniprot_1': None, 'protein_1_gene_name': None, 'tags_1': None, 'entry_name_1': None,
            'tags_description_1': None, 'tags_reason_1': None,
            'uniprot_2': None, 'protein_2_gene_name': None, 'tags_2': None, 'entry_name_2': None,
            'tags_description_2': None, 'tags_reason_2': None,
            'uniprot_3': None, 'protein_3_gene_name': None, 'tags_3': None, 'entry_name_3': None,
            'tags_description_3': None, 'tags_reason_3': None,
            'uniprot_4': None, 'protein_4_gene_name': None, 'tags_4': None, 'entry_name_4': None,
            'tags_description_4': None, 'tags_reason_4': None,
        }
        for index, complex_composition in complex_complex_composition.iterrows():
            proteine_name = \
                multidatas[multidatas['id_multidata'] == complex_composition['protein_multidata_id']][
                    'name'].values[0]
            complex_proteins['uniprot_%i' % protein_index] = proteine_name

            selected_protein = proteins[proteins['name'] == proteine_name]
            entry_name = selected_protein['entry_name'].values[0]
            complex_proteins['protein_%i_gene_name' % protein_index] = entry_name
            complex_proteins['entry_name_%i' % protein_index] = entry_name
            complex_proteins['tags_%i' % protein_index] = selected_protein['tags'].values[0]
            complex_proteins['tags_description_%i' % protein_index] = selected_protein['tags_description'].values[0]
            complex_proteins['tags_reason_%i' % protein_index] = selected_protein['tags_reason'].values[0]
            protein_index += 1


        composition.append(complex_proteins)

    composition_df = pd.DataFrame(composition)
    complex_complete = pd.merge(complex_complete, composition_df, on='complex_multidata_id')
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
