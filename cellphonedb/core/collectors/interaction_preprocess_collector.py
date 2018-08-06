import pandas as pd

from cellphonedb.core.models.interaction import interaction_properties
from utils import unique_id_generator


def call(interactions: pd.DataFrame, multidatas: pd.DataFrame) -> pd.DataFrame:
    interactions_processed = interactions.fillna({'dlrp': False, 'iuphar': False})

    interactions_processed = _set_interactor_property(interactions_processed, multidatas)

    return interactions_processed


def _set_interactor_property(interactions_processed: pd.DataFrame,
                             multidatas: pd.DataFrame) -> pd.DataFrame:
    interactions_processed_expanded = pd.merge(interactions_processed, multidatas, left_on=['multidata_name_1'],
                                               right_on=['name'])
    interactions_processed_expanded = pd.merge(interactions_processed_expanded, multidatas,
                                               left_on=['multidata_name_2'], right_on=['name'],
                                               suffixes=['_x', '_y'])
    interactions_processed_expanded['is_cellphonedb_interactor'] = interactions_processed_expanded.apply(
        lambda interaction: interaction_properties.is_cellphonedb_interactor(interaction, ('_x', '_y')), axis=1)

    interactions_processed_expanded['id_cp_interaction'] = interactions_processed_expanded.apply(
        lambda interaction: unique_id_generator.interaction(interaction, ('_x', '_y')), axis=1)

    return interactions_processed_expanded
