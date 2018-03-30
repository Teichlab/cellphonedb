#!/usr/bin/env bash
# Run flask app before: export FLASK_APP=manage.py; flask run


# Cluster Receptor Ligand Processed
curl -i \
     -F "cell_to_clusters_file=@in/example_data/cells_to_clusters.csv;type=text/csv" \
     -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
     http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions

# Cluster Receptor Ligand Unprocessed
curl -i \
    -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
    -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
    -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
    http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions_unprocessed

# Fast query
curl -i \
     --data "{\"receptor\": \"P25106\"}" \
     http://127.0.0.1:5000/api/get_ligands_from_receptor


