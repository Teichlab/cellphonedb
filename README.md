# CellPhoneDB

A Collection of cellular communication data

## Requirements

CellPhoneDB needs some external software before start working. Plese, verify if you have it installed in your system:
```
- Python 3.x
- Pip
- Docker or PostgreSQL 9.X
```

## Installing

Firstly, clone this repo in your system or download the code

    git clone https://github.com/Teichlab/cellphonedb.git
    cd cellphonedb


Install the dependencies as specified in the requirements.txt file (tip! to avoid compatibility problems, we recommend that you create a [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/) )

    pip install -r requirements.txt

**Only if you are using Docker** Create Docker and start PostgreSQL instance

    docker-compose build

CellPhoneDB requires environment variables to configure it. Please configure it:
These can be added to your `.bashrc` or your virtual environment startup script.
Note that you may need to add this directory to your `PYTHONPATH` environmental variable.

    export FLASK_APP=manage.py
    
    export APP_CONF_SUPPORT=yaml
    export APP_LOAD_DEFAULTS=true
    export APP_ENV=local

Populate the database

    python flask collect all

## Using CellPhoneDB

**Only if you are using Docker** Start docker container

    docker-compose start

Run CellPhoneDB

    flask run


## Doing Requests
- Before start making requests from Python/API Rest, you need to [start the server](#using-cellphonedb).
- For make a request from the terminal, please open other terminal window.
- For Terminal API, check out/ folder to check the results.


From **Python** (ALPHA)

Edit ```api_interfaces/python/cellphone.py``` file (after ```if __name__ == '__main__':```) with your requests and run it:

You can save your input data in api_interfaces/python/input_data and view results in api_interfaces/python/out

    cd api_interfaces/python
    python cellphone.py


### Get Receptor-Ligand/Ligand-Receptor interactions
From **Terminal**:
   
    flask call_query get_rl_lr_interactions {{ uniprot|entry_name|gene_name|ensembl|complex_name }} [enable_integrin=1 [min_score_2=0.2]]
    
Example
   
    flask call_query get_rl_lr_interactions P05107 1 0.2

From **API REST**

    curl -i \
         --data "{\"receptor\": \"{{ uniprot|entry_name|gene_name|ensembl|complex_name }}\"}" \
         http://127.0.0.1:5000/api/get_ligands_from_receptor

Example:

    curl -i \
        --data "{\"receptor\": \"P25106\"}" \
        http://127.0.0.1:5000/api/get_ligands_from_receptor



### Cluster Receptor Ligand Unprocessed Query
From **Terminal**

    flask call_query cluster_receptor_ligand_interactions_unprocessed meta_file {{ counts_file }} [threshold=0.2]


Example

    flask call_query cluster_receptor_ligand_interactions_unprocessed example_data/test_meta.txt example_data/test_counts.txt 0.2

From **API REST**
    
    curl -i \
        -F "counts_file=@{{ counts_file }};type={{ counts mime_type }}" \
        -F "meta_file=@{{ meta_file }};type={{ meta mime_type }}" \
        -F parameters="{\"threshold\": {{ threshold }}, \"enable_integrin\": \"{{ true|false }}\"}" \
        http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions_unprocessed

Example
       
    curl -i \
        -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
        -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
        -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
        http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions_unprocessed

### Cell to Clusters Query

From **Terminal**

    flask call_query cells_to_clusters {{ meta_file }} {{ counts_file }}

Example

    flask call_query cells_to_clusters example_data/test_meta.txt example_data/test_counts.txt

From **API REST** 

    curl -i \
        -F "counts_file=@{{ counts_file }};type={{ counts mime_type }}" \
        -F "meta_file=@{{ meta_file }};type={{ meta mime_type }}" \
        http://127.0.0.1:5000/api/cell_to_cluster

Example

    curl -i \
        -F "counts_file=@in/example_data/test_counts.txt;type=text/tab-separated-values" \
        -F "meta_file=@in/example_data/test_meta.txt;type=text/tab-separated-values" \
        http://127.0.0.1:5000/api/cell_to_cluster
### Cluster Receptor Ligand Processed Query

From **Terminal**

    flask call_query cluster_receptor_ligand_interactions {{ cell_to_cluster_file }} [threshold=0.2]
    
Example

    flask call_query cluster_receptor_ligand_interactions example_data/cells_to_clusters.csv 0.2


From **API REST** 

    curl -i \
         -F "cell_to_clusters_file=@{{ cells_to_cluster_file }};type={{ mime_type }}" \
         -F parameters="{\"threshold\": {{ threshold }}, \"enable_integrin\": \"{{ true|false }}\"}" \
         http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions


Example:

    curl -i \
         -F "cell_to_clusters_file=@in/example_data/cells_to_clusters.csv;type=text/csv" \
         -F parameters="{\"threshold\": 0.2, \"enable_integrin\": \"true\"}" \
         http://127.0.0.1:5000/api/cluster_receptor_ligand_interactions
        


## Useful commands

### Downloading tools data

This repository uses git lfs to store the large data files used to populate the database.
Information on using and installing git lfs can be found [here](https://git-lfs.github.com/).
Once installed, you can download the data files using the following.

    git lfs pull

### Creating Docker Container
    docker-compose up -d

### Creating database structure
    python flask create_db

## Running Docker Container
    docker-compose start
    
## Stopping Docker Container
    docker-compose stop

## Reseting Database
    python flask reset_db
    
## Populating the database

    python flask collect protein

## Exporting database table

You can export datatabase tables to csv, calling the export method. Outout is stored in out folder.

    python flask export protein
    
## Running the debug server

The debug server runs over port 5000

    python flask run

Then, You will then be able to query the rest api:


## Running tests

### All tests
    python -m unittest discover
    