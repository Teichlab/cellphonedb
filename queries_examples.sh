#!/usr/bin/env bash
# Run flask app before: export FLASK_APP=manage.py flask run

export FLASK_APP=manage.py

# Cluster Receptor Ligand Processed
## Terminal API

flask call_query cluster_receptor_ligand_interactions example_data/cells_to_clusters.csv 0.2

## API Rest
curl -i \
     -F "cell_to_clusters_file=@in/example_data/cells_to_clusters.csv;type=text/csv" \
     -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
     http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions

# Cluster Receptor Ligand Unprocessed
## Terminal API
flask call_query cluster_receptor_ligand_interactions_unprocessed example_data/test_meta.txt example_data/test_counts.txt 0.2

## API Rest
curl -i \
    -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
    -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
    -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
    http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions_unprocessed

# Fast query
## Terminal API
flask call_query get_rl_lr_interactions P05107 1 0.2


## API Rest
curl -i \
     --data "{\"receptor\": \"P05107\"}" \
     http://127.0.0.1:5000/api/get_ligands_from_receptor



# Cells to Clusters
## Terminal API
flask call_query cells_to_clusters example_data/test_meta.txt example_data/test_counts.txt

## API Rest

curl -i \
    -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
    -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
    http://127.0.0.1:5000/api/cell_to_cluster
