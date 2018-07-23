import pandas as pd


def call(multidatas: pd.DataFrame, interactions: pd.DataFrame):
    interactions_filtered = interactions[interactions['is_cellphonedb_interactor']]

    multidatas_interactors_ids = interactions_filtered['multidata_1_id'].append(
        interactions_filtered['multidata_2_id']).drop_duplicates().reset_index(drop=True).tolist()

    multidatas_filtered = multidatas[multidatas['id_multidata'].apply(lambda id: id in multidatas_interactors_ids)]

    return multidatas_filtered[
        ['name', 'entry_name', 'transmembrane', 'secretion', 'peripheral', 'integrin_interaction', 'secreted_highlight',
         'secreted_desc', 'transporter', 'other', 'other_desc', 'tags', 'tags_description', 'tags_reason']]
