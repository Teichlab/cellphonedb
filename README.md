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

Firstly, clone this repo in your system

    git clone https://github.com/Teichlab/cellcommdb.git
    cd cellcommdb


Install the dependencies as specified in the requirements.txt file

    pip install -r requirements.txt

Create Docker and start PostgreSQL instance

    docker-compose build

CellPhoneDB requires environment variables to configure it. Please configure it:
These can be added to your `.bashrc` or your virtual environment startup script.
Note that you may need to add this directory to your `PYTHONPATH` environmental variable.

    export FLASK_APP=manage.py
    export APP_CONF_SUPPORT=yaml
    export APP_LOAD_DEFAULTS=true
    export APP_ENV=local

Populate the database

    python manage.py collect all

## Using CellPhoneDB

Start docker container

    docker-compose start

Run CellPhoneDB

    flask run


## Doing Requests
Doing queries (please open other terminal tab/window)

### Get Receptor-Ligand/Ligand-Receptor interactions
From Terminal:

    flask call_query get_rl_lr_interactions ACKR3_HUMAN 0.3

From Python (Alpha Verion, while github was not public)

Edit ```api_interfaces/python/cellphone``` file (after ```if __name__ == '__main__':```) with your requests and run it:

You can save your input data in api_interfaces/python/input_data and view results in api_interfaces/python/out

    cd api_interfaces/python
    python cellphone.py


## Useful commands

### Downloading tools data

This repository uses git lfs to store the large data files used to populate the database.
Information on using and installing git lfs can be found [here](https://git-lfs.github.com/).
Once installed, you can download the data files using the following.

    git lfs pull

### Creating Docker Container
    docker-compose up -d

### Creating database structure
    python manage.py create_db

## Running Docker Container
    docker-compose start
    
## Stopping Docker Container
    docker-compose stop

## Reseting Database
    python manage.py reset_db
    
## Populating the database

The data import files are called through the `manage.py` script.

    python manage.py collect protein

## Exporting database table

You can export datatabase tables to csv, calling the export method. Outout is stored in out folder.

    python manage.py export protein
    
## Running the debug server

The debug server is also started using the `manage.py` script (default port 5000)

    python manage.py run

You will then be able to query the api:

    $ curl localhost:5000/api/protein?id=1
    [
        {
            "adhesion": false,
            "entry_name": "AAMP_HUMAN",
            "id": 1,
            "other": false,
            "other_desc": null,
            "peripheral": false,
            "receptor": false,
            "receptor_desc": null,
            "receptor_highlight": false,
            "secreted_desc": null,
            "secreted_highlight": false,
            "secretion": false,
            "tags": null,
            "tags_reason": null,
            "transmembrane": true,
            "transporter": false,
            "uniprot": "Q13685"
        }
    ]    


## Running tests

The resources can be tested by running the resource test script:

    python cellcommdb/tests/test_resources.py

### All tests
    python -m unittest discover
    
### Single test module ex.
    python -m unittest cellcommdb.tests.test_resources
    
### Single test case or method
    python -m unittest cellcommdb.tests.test_resources.TestResource
    python -m unittest cellcommdb.tests.test_resources.TestResource.test_protein
