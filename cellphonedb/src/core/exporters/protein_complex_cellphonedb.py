import pandas as pd


def call(multidatas: pd.DataFrame, interactions: pd.DataFrame):
    multidatas_interactors_ids = interactions['multidata_1_id'].append(
        interactions['multidata_2_id']).drop_duplicates().reset_index(drop=True).tolist()

    multidatas_filtered = multidatas[multidatas['id_multidata'].apply(lambda id: id in multidatas_interactors_ids)]

    return multidatas_filtered[
        ['name', 'protein_name', 'transmembrane', 'secreted', 'peripheral', 'integrin',
         'secreted_highlight',
         'secreted_desc', 'other', 'other_desc', 'tags', 'tags_description', 'tags_reason']]
