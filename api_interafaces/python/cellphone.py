import email
import json

import requests

import pandas as pd


def cells_to_clusters(meta, counts):
    """

    :type meta: pd.DataFrame
    :type counts: pd.DataFrame
    :rtype: pd.DataFrame
    """

    url = 'http://localhost:5000/api/cell_to_cluster'

    files = {
        'meta_file': ('meta.csv', meta.to_csv(), 'text/csv'),
        'counts_file': ('counts.csv', counts.to_csv(), 'text/csv'),
    }
    response = requests.post(url, files=files)

    response_body = email.message_from_string(response.text)
    response_body = [i for i in response_body.walk()]

    status = json.loads(response_body[1].get_payload())

    if 'errors' in status:
        raise Exception(status['errors'])

    cells_clusters_raw = response_body[2].get_payload()

    cells_clusters = pd.read_csv(pd.compat.StringIO(cells_clusters_raw), index_col=0)

    return cells_clusters


def receptor_ligands_interactions_request(cells_clusters, threshold=0.1):
    """

    :type cells_clusters: pd.DataFrame
    :type threshold: float
    :rtype: (pd.DataFrame, pd.DataFrame)

    """
    url = 'http://localhost:5000/api/receptor_ligands_interactions'

    files = {'cell_to_clusters_file': (
        'cells_to_clusters.csv', cells_clusters.to_csv(), 'text/csv')}

    response = requests.post(url, files=files, data={'parameters': json.dumps({'threshold': threshold})})

    response_body = email.message_from_string(response.text)
    response_body = [i for i in response_body.walk()]

    status = json.loads(response_body[1].get_payload())

    if 'errors' in status:
        raise Exception(status['errors'])

    interactions_raw = response_body[2].get_payload()
    interactions_extended_raw = response_body[3].get_payload()

    interactions = pd.read_table(pd.compat.StringIO(interactions_raw))
    interactions_extended = pd.read_table(pd.compat.StringIO(interactions_extended_raw))
    return interactions, interactions_extended


def get_ligands_from_receptor(receptor: str) -> pd.DataFrame:
    url = 'http://localhost:5000/api/get_ligands_from_receptor'

    response = requests.post(url, data=json.dumps({'receptor': receptor}))

    response_body = email.message_from_string(response.text)
    response_body = [i for i in response_body.walk()]

    status = json.loads(response_body[1].get_payload())

    if 'errors' in status:
        raise Exception(status['errors'])

    ligands_raw = response_body[2].get_payload()

    ligands = pd.read_table(pd.compat.StringIO(ligands_raw))

    return ligands


def cells_to_clusters_example():
    meta = pd.read_table('cellcommdb/data/queries/test_meta.txt', index_col=0)
    counts = pd.read_table('cellcommdb/data/queries/test_counts.txt', index_col=0)
    cells_clusters = cells_to_clusters(meta, counts)
    cells_clusters.to_csv('out/API_cells_clusters.csv')
    print(cells_clusters)


def receptor_ligands_interactions_example():
    cells_clusters = pd.read_csv('out/API_cells_clusters.csv', index_col=0)
    threshold = 0.1
    receptor_ligands_interactions, receptor_ligands_interactions_extended = receptor_ligands_interactions_request(
        cells_clusters, threshold)

    receptor_ligands_interactions.to_csv('out/API_receptor_ligands_interactions.csv', index=False)
    receptor_ligands_interactions_extended.to_csv('out/API_receptor_ligands_interactions_extended.csv', index=False)
    print(receptor_ligands_interactions)
    print(receptor_ligands_interactions_extended)


if __name__ == '__main__':
    cells_to_clusters_example()
    receptor_ligands_interactions_example()
    print(get_ligands_from_receptor('P25106'))
