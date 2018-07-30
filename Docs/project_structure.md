# CellPhoneDB Project Structure

This is the CelPhoneDB basic project structure

```
+-- cellphonedb
|   +-- api_endpoints
|   |   +-- terminal_api
|   |   +-- web_api
|   +-- app
|   +-- config
|   +-- core
|   |   +-- collectors
|   |   +-- data
|   |   +-- database
|   |   +-- exporters
|   |   +-- methods
|   |   +-- models
|   |   +-- queries
|   |   +-- repository
|   |   +-- tests
|   |   +-- utils
|   |   +-- cellphone.db
|   |   +-- cellphonedb.py
|   |   +-- CellphonedbSqlalchemy.py
|   |   +-- core_logger.py
|   +-- flask_cellphonedb
|   +-- tests
+-- Docs
+-- in
+-- out
+-- tools
|   +-- actions
|   +-- data
|   +-- generate_data
|   +-- out
|   +-- repository
|   +-- validators
|   +-- app.py
|   +-- interaction_actions.py
|   +-- merged_duplicated_proteins.py
|   +-- set_protein_type.py
+-- utils
+-- cellphonedb.ini
+-- MANIFEST.in
+-- setup.py
+-- tools.py
+-- wsgi.py

```

## Explanation by path
### cellphonedb
This folder contains the project files. 

**api_endpoints** 
This is where api_endpoints (web/terminal) are defined.

If you need to add terminal 