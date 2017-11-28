import pandas as pd


def call(counts, meta):
    clusters = _create_clusters_structure(counts, meta)

    return _clusters_ratio(clusters)


def _clusters_ratio(clusters):
    all_cells_names = next(iter(clusters.values())).index

    result = pd.DataFrame(0.0, all_cells_names, sorted(list(clusters.keys())))
    for cluster_name in clusters:
        print('Transforming Cluster %s' % cluster_name)
        cluster = clusters[cluster_name]

        cells_names = cluster.columns.values
        for gene_name in cluster.index:
            positives = 0

            for cell_name in cells_names:
                count_value = cluster.loc[gene_name, cell_name]

                if count_value > 0:
                    positives = positives + 1

            result.set_value(gene_name, cluster_name, positives / len(cells_names))
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
