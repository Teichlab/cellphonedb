import pandas as pd

from cellphonedb.src.core.models.interaction import interaction_properties


def filter_by_cellphonedb_interactor(uniprots: pd.DataFrame, interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_filtered = pd.merge(interactions, uniprots, left_on=['protein_1'], right_on=['uniprot'], how='inner')

    interactions_filtered = pd.merge(interactions_filtered, uniprots, left_on=['protein_2'],
                                     right_on=['uniprot'], how='inner', suffixes=('_1', '_2'))

    interactions_filtered.rename(columns={'uniprot_1': 'id_multidata_1', 'uniprot_2': 'id_multidata_2'}, inplace=True)
    interactions_filtered.drop_duplicates(inplace=True)

    interactions_filtered = interactions_filtered[
        interactions_filtered.apply(lambda interaction: interaction_properties.is_cellphonedb_interactor(interaction),
                                    axis=1)]

    return interactions_filtered[interactions.columns.values]
