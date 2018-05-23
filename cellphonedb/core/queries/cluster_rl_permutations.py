import pandas as pd

from cellphonedb.core.models.interaction import filter_interaction
from cellphonedb.core.queries import cluster_rl_permutations_complex


def call(meta: pd.DataFrame, counts: pd.DataFrame, interactions: pd.DataFrame, iterations: int = 1000,
         debug_mode: bool = False, threshold: float = 0.3) -> (pd.DataFrame, pd.DataFrame):
    # TODO: Check interactions with multiple genes

    interactions_filtered, counts_filtered = prefilters(counts, interactions)

    interactions_filtered.drop_duplicates('id_interaction', inplace=True)

    clusters = build_clusters(meta, counts_filtered, threshold)
    cluster_interactions = cluster_rl_permutations_complex.get_cluster_combinations(clusters['names'])

    base_result = cluster_rl_permutations_complex.build_result_matrix(interactions_filtered, cluster_interactions)

    real_mean_analysis = cluster_rl_permutations_complex.mean_analysis(interactions_filtered, clusters,
                                                                       cluster_interactions, base_result,
                                                                       suffixes=('_receptor', '_ligand'))

    real_percent_analysis = cluster_rl_permutations_complex.percent_analysis(clusters, threshold, interactions_filtered,
                                                                             cluster_interactions, base_result,
                                                                             suffixes=('_receptor', '_ligand'))

    statistical_mean_analysis = cluster_rl_permutations_complex.shuffled_analysis(iterations, meta, counts_filtered,
                                                                                  interactions_filtered,
                                                                                  cluster_interactions, base_result,
                                                                                  suffixes=('_receptor', '_ligand'))

    result_percent = cluster_rl_permutations_complex.build_percent_result(real_mean_analysis, real_percent_analysis,
                                                                          statistical_mean_analysis,
                                                                          interactions_filtered,
                                                                          cluster_interactions, base_result)

    return real_mean_analysis, result_percent


def shuffle_meta(meta: pd.DataFrame) -> pd.DataFrame:
    pd.np.random.shuffle(meta['cell_type'])

    return meta


def build_clusters(meta: pd.DataFrame, counts: pd.DataFrame, threshold: float) -> dict:
    cluster_names = meta['cell_type'].drop_duplicates().tolist()
    clusters = {'names': cluster_names, 'counts': {}, 'means': {}, 'percents': {}}

    cluster_counts = {}
    cluster_means = {}
    cluster_percent = {}

    for cluster_name in cluster_names:
        cells = meta[meta['cell_type'] == cluster_name].index
        cluster_count = counts.loc[:, cells]
        cluster_counts[cluster_name] = cluster_count
        cluster_means[cluster_name] = cluster_count.apply(lambda counts: counts.mean(), axis=1)

        def counts_percent(counts, threshold):
            total = len(counts)
            positive = len(counts[counts > 0])

            if positive / total < threshold:
                return 0
            else:
                return 1

        cluster_percent[cluster_name] = cluster_count.apply(lambda counts: counts_percent(counts, threshold),
                                                            axis=1)

    clusters['counts'] = cluster_counts
    clusters['means'] = cluster_means
    clusters['percents'] = cluster_percent

    return clusters


def prefilters(counts: pd.DataFrame, interactions: pd.DataFrame):
    interactions_filtered = filter_interaction.filter_by_receptor_ligand_ligand_receptor(interactions,
                                                                                         enable_integrin=False,
                                                                                         avoid_duplited=False,
                                                                                         avoid_duplicated_genes=False)

    counts_filtered = filter_counts_by_interactions(counts, interactions)
    counts_filtered = filter_empty_cluster_counts(counts_filtered)
    interactions_filtered = filter_interactions_by_counts(interactions_filtered, counts_filtered,
                                                          ('_receptor', '_ligand'))
    interactions_filtered = filter_interactions_non_individual(interactions_filtered, ('_receptor', '_ligand'))

    # TODO: waiting for aproval. What happens when there are duplicated interactions (gene-gene)? Remove duplicates its a temp solution
    interactions_filtered = interactions_filtered[
        ~interactions_filtered.duplicated(['ensembl_receptor', 'ensembl_ligand'], keep='first')]

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


def filter_counts_by_interactions(counts: pd.DataFrame, interactions: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    genes = interactions['ensembl{}'.format(suffixes[0])].append(
        interactions['ensembl{}'.format(suffixes[1])]).drop_duplicates()

    counts_filtered = counts.filter(genes, axis=0)

    return counts_filtered


def filter_interactions_by_counts(interactions: pd.DataFrame, counts: pd.DataFrame,
                                  suffixes: tuple = ('_1', '_2')) -> pd.DataFrame:
    ensembl_counts = list(counts.index)
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
