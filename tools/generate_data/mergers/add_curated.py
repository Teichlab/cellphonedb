import pandas as pd

from tools.generate_data.mergers import merge_interactions
from tools.tools_helper import normalize_interactions


def add_curated(interactions: pd.DataFrame, interaction_curated: pd.DataFrame) -> pd.DataFrame:
    interactions.rename(index=str, columns={'uniprot_1': 'multidata_name_1', 'uniprot_2': 'multidata_name_2'},
                        inplace=True)

    interactions_curated_normalized = normalize_interactions(interaction_curated, 'multidata_name_1',
                                                             'multidata_name_2')
    curated_duplicated = interactions_curated_normalized[
        interactions_curated_normalized.duplicated(['multidata_name_1', 'multidata_name_2'], keep=False)]

    if not curated_duplicated.empty:
        print(
            'WARNING - Some curated interactions are duplicated.')
        print(interaction_curated.iloc[
            curated_duplicated.sort_values(['multidata_name_1', 'multidata_name_2']).index.values].to_csv(
            index=False))
    interactions.rename(index=str, columns={'protein_1': 'multidata_name_1', 'protein_2': 'multidata_name_2'},
                        inplace=True)

    interaction_curated_result = merge_interactions.merge_iuphar_other_and_curated_interactions(interactions,
                                                                                                interaction_curated)

    return interaction_curated_result
