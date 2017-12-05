import pandas as pd


def call(counts, meta):
    clusters = _create_clusters_structure(counts, meta)

    return _clusters_ratio(clusters)


def _clusters_ratio(clusters):
    all_cells_names = next(iter(clusters.values())).index

    result = pd.DataFrame(None, all_cells_names)
    for cluster_name in clusters:
        print('Transforming Cluster %s' % cluster_name)
        cluster = clusters[cluster_name]

        cells_names = cluster.columns.values
        number_cells = len(cells_names)
        cluster_count_value = cluster.apply(lambda row: sum(row.astype('bool')) / number_cells, axis=1)
        result[cluster_name] = cluster_count_value

    return result


def _create_clusters_structure(counts, meta):
    print('Creating Cluster Structure')
    cluster_names = meta['cell_type'].unique()

    print(cluster_names)
    clusters = {}
    for cluster_name in cluster_names:
        cluster_cell_names = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % cluster_name)]).index
        clusters[cluster_name] = counts.loc[:, cluster_cell_names]

    return clusters
