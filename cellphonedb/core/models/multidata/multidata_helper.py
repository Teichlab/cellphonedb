import pandas as pd


def get_multidatas_from_interactions(interactions: pd.DataFrame, multidatas: pd.DataFrame) -> pd.DataFrame:
    interaction_multidatas = pd.DataFrame(
        interactions['multidata_1_id'].append(interactions['multidata_2_id']).drop_duplicates(),
        columns=['id_multidata'])

    result = multidatas.merge(interaction_multidatas, on='id_multidata')

    return result
