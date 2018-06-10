import pandas as pd


def call(interactions: pd.DataFrame) -> pd.DataFrame:
    interactions_processed = interactions.fillna({'dlrp': False, 'iuhpar': False})

    return interactions_processed
