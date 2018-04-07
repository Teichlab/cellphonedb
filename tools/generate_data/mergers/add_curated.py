import pandas as pd

from tools.generate_data.mergers.merge_interactions import merge_interactions
from tools.repository.interaction import normalize_interactions


def add_curated(interactions: pd.DataFrame, interaction_curated: pd.DataFrame) -> pd.DataFrame:
    interactions.rename(index=str, columns={'uniprot_1': 'multidata_name_1', 'uniprot_2': 'multidata_name_2'},
                        inplace=True)
    interactions_curated_normalized = normalize_interactions(interaction_curated, 'multidata_name_1',
                                                             'multidata_name_2')
    curated_duplicated = interactions_curated_normalized[
        interactions_curated_normalized.duplicated(['multidata_name_1', 'multidata_name_2'])]

    if not curated_duplicated.empty:
        print(
            'WARNING - Some curated interactions are duplicated. Please check WARNING_curated_interactions_duplicated.csv file')
        curated_duplicated.to_csv('out/WARNING_curated_interactions_duplicated.csv', index=False)
    interactions.rename(index=str, columns={'protein_1': 'multidata_name_1', 'protein_2': 'multidata_name_2'},
                        inplace=True)

    interaction_curated = merge_interactions(interactions_curated_normalized, interactions, 'multidata_name_1',
                                             'multidata_name_2')

    return interaction_curated
