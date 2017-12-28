import pandas as pd

from tools.generate_data.mergers.merge_interactions import merge_interactions


def add_curated(interactions: pd.DataFrame, interaction_curated: pd.DataFrame) -> pd.DataFrame:
    interactions.rename(index=str, columns={'protein_1': 'multidata_name_1', 'protein_2': 'multidata_name_2'},
                        inplace=True)

    interaction_curated = merge_interactions(interaction_curated, interactions, 'multidata_name_1', 'multidata_name_2')
    return interaction_curated
