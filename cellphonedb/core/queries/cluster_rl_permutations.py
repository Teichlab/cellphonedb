import itertools

import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         debug_mode: bool = False) -> (pd.DataFrame, pd.DataFrame):
    # TODO: Check interactions with multiple genes
    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    print(len(interactions_filtered))
    print(len(counts_filtered))

    return (pd.DataFrame(), pd.DataFrame())


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame):
    interactions_filtered = filter_interaction.filter_by_receptor_ligand_ligand_receptor(interactions,
                                                                                         enable_integrin=False,
                                                                                         avoid_duplited=True)
    counts_filtered = filter_counts_by_interactions(counts, interactions)
    counts_filtered = filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = filter_interactions_by_counts(interactions_filtered, counts_filtered,
                                                          ('_receptor', '_ligand'))
    interactions_filtered = filter_interactions_non_individual(interactions_filtered, ('_receptor', '_ligand'))
    counts_filtered = filter_counts_by_interactions(counts_filtered, interactions_filtered, ('_receptor', '_ligand'))

    return interactions_filtered, counts_filtered


def filter_empty_cluster_counts(counts: pd.DataFrame) -> pd.DataFrame:
    """
    Removes counts with all values to zero
    """
    if counts.empty:
        return counts

    filtered_counts = counts[counts.apply(lambda row: row.sum() > 0, axis=1)]
    return filtered_counts


def get_cluster_combinations(cluster_names):
    return list(itertools.product(cluster_names, repeat=2))


def cluster_analysis(interactions: pd.DataFrame):
    for interaction_index, interaction in interactions.iterrows():
        pass


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    ensembl_counts = counts.index
    interactions_filtered = interactions[interactions.apply(
        lambda row: row['ensembl{}'.format(suffixes[0])] in ensembl_counts and row[
            'ensembl{}'.format(suffixes[1])] in ensembl_counts, axis=1
    )]
    return interactions_filtered


def filter_interactions_non_individual(interactions: pd.DataFrame, suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    interactions_filtered = interactions[
        interactions.apply(lambda interaction: interaction['ensembl{}'.format(suffixes[0])] != interaction[
            'ensembl{}'.format(suffixes[1])], axis=1)]

    return interactions_filtered
