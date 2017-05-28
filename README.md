# cellcommdb

A Collection of cellular communication data

## Installing

Firstly, install the dependencies as specified in the requirements.txt file

    pip install -r requirements.txt

Cellcommdb looks for the sqlalchemy connection string in the environmental variables.
Make sure you set them appropriately for the production and test servers, for example:

    export CELLCOMMDB_URI="postgresql+psycopg2://user:password@localhost:5432/cellcommdb
    export CELLCOMMDB_TEST_URI="postgresql+psycopg2://user:password@localhost:5432/test

These can be added to your `.bashrc` or your virtual environment startup script.
Note that you may need to add this directory to your `PYTHONPATH` environmental variable.

### Downloading the database data

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
