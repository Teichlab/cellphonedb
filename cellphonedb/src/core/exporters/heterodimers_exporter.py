import pandas as pd

from cellphonedb.src.core.exporters import complex_exporter


def call(complexes: pd.DataFrame, multidatas: pd.DataFrame, complex_compositions: pd.DataFrame,
         proteins: pd.DataFrame) -> pd.DataFrame:
    result = complex_exporter.call(complexes, multidatas, complex_compositions, proteins)

    return result[['name', 'transmembrane', 'secreted', 'peripheral', 'integrin', 'secreted_highlight',
                   'secreted_desc', 'transporter', 'other', 'other_desc',
                   'protein_name_1', 'uniprot_1', 'tags_1', 'tags_description_1', 'tags_reason_1',
                   'protein_name_2', 'uniprot_2', 'tags_2', 'tags_description_2', 'tags_reason_2',
                   'protein_name_3', 'uniprot_3', 'tags_3', 'tags_description_3', 'tags_reason_3',
                   'protein_name_4', 'uniprot_4', 'tags_4', 'tags_description_4', 'tags_reason_4',
                   'pdb_structure', 'pdb_id', 'stoichiometry', 'comments_complex']]
