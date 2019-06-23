import pandas as pd

from cellphonedb.utils import dataframe_format


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
            'uniprot_1': None, 'protein_1_gene_name': None, 'tags_1': None, 'protein_name_1': None,
            'tags_description_1': None, 'tags_reason_1': None,
            'uniprot_2': None, 'protein_2_gene_name': None, 'tags_2': None, 'protein_name_2': None,
            'tags_description_2': None, 'tags_reason_2': None,
            'uniprot_3': None, 'protein_3_gene_name': None, 'tags_3': None, 'protein_name_3': None,
            'tags_description_3': None, 'tags_reason_3': None,
            'uniprot_4': None, 'protein_4_gene_name': None, 'tags_4': None, 'protein_name_4': None,
            'tags_description_4': None, 'tags_reason_4': None,
        }
        for index, complex_composition in complex_complex_composition.iterrows():
            proteine_name = \
                multidatas[multidatas['id_multidata'] == complex_composition['protein_multidata_id']][
                    'name'].values[0]
            complex_proteins['uniprot_%i' % protein_index] = proteine_name

            selected_protein = proteins[proteins['name'] == proteine_name]
            protein_name = selected_protein['protein_name'].values[0]
            complex_proteins['protein_%i_gene_name' % protein_index] = protein_name
            complex_proteins['protein_name_%i' % protein_index] = protein_name
            complex_proteins['tags_%i' % protein_index] = selected_protein['tags'].values[0]
            complex_proteins['tags_description_%i' % protein_index] = selected_protein['tags_description'].values[0]
            complex_proteins['tags_reason_%i' % protein_index] = selected_protein['tags_reason'].values[0]
            protein_index += 1


        composition.append(complex_proteins)

    composition_df = pd.DataFrame(composition)
    complex_complete = pd.merge(complex_complete, composition_df, on='complex_multidata_id')

    complex_complete.rename({'name': 'complex_name'}, axis=1, inplace=1)

    return complex_complete[
        ['complex_name', 'uniprot_1', 'uniprot_2', 'uniprot_3', 'uniprot_4', 'transmembrane', 'peripheral', 'secreted',
         'secreted_desc', 'secreted_highlight', 'receptor', 'receptor_desc', 'integrin', 'other', 'other_desc',
         'pdb_id', 'pdb_structure', 'stoichiometry', 'comments_complex']]
