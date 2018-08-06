# CellPhoneDB Project Structure

This is the CelPhoneDB basic project structure

```
+-- cellphonedb
|   +-- api_endpoints
|   |   +-- terminal_api
|   |   +-- web_api
|   +-- app
|   |   +-- config
|   |   +-- flask
|   |   +-- app_config.py
|   |   +-- app_logger.py
|   |   +-- cellphonedb_app.py
|   +-- core
|   |   +-- collectors
|   |   +-- data
|   |   +-- database
|   |   |   +-- sqlalchemy_repository
|   |   |   +-- sqlalchemy_models
|   |   +-- exporters
|   |   +-- methods
|   |   +-- models
|   |   +-- queries
|   |   +-- tests
|   |   +-- utils
|   |   +-- cellphone.db
|   |   +-- cellphonedb.py
|   |   +-- CellphonedbSqlalchemy.py
|   |   +-- core_logger.py
|   +-- local_launchers
|   +-- tests
+-- Docs
+-- in
+-- out
+-- tools
|   +-- actions
|   +-- data
|   +-- generate_data
|   +-- out
|   +-- validators
|   +-- app.py
|   +-- interaction_actions.py
|   +-- merged_duplicated_proteins.py
|   +-- tools_helper.py
+-- manage.py
+-- utils
+-- cellphonedb.ini
+-- MANIFEST.in
+-- setup.py
+-- tools.py
+-- wsgi.py

```

## cellphonedb
This folder contains the project files. 

**api_endpoints**
 
This is where api_endpoints (web/terminal) are defined. 

**app/config**

Contains the configs of database/debug for different scenarios. 
You can create new one and use it setting the APP_ENV environment variable.


**app/flask**

Contains flask app files.

**app/app_config.py**

Loads the app config from _app/config_ or environment variables.

**app/app_logger.py**

Logging implementation for cellphone app logs.

**app/cellphonedb_app.py**

CellPhoneDB App instance.

**core**

Core package contains all CellPhoneDB business logic. It din't have dependence from the rest of the project.

**core/collectors**

- _collector.py_: Saves the input data in the database. If is it necessary, calls to the data preprocessors. 
- _{some}_preprocess_collector.py_: Process the data when is it necessary (ie: for rename columns, create optimizations, etc.)

**core/data** 

CellPhoneDB import data. This are the files used to load the internal CellPhoneDB data.

Insert the new lists here when you need to update the CellPhoneDB database (interactions/proteins/gens/complex)

**core/database**

Database manage files. Isolates the database orm to the rest of the project. This files manages the different orms and orchestrates the data repositories

**core/database/sqlalchemy_repository**

Data access isolation. This is where are allocated the orm calls. The prefix  (_sqlalchemy_ in this case) is the orm used.

**code/database/sqlalchemy_models**

Data models isolation. This is where SqlAlchemy models are defined. 

**core/exporters**

Export data functions. Here is where allocated the database exporters. Usually the data is preprocessed before dump it (ie: complex needs to be exported in just one file but in the database are defined from multiple files)

**core/methods**

This is where are implemented the CellPhoneDB Methods. One method is like a query but with more data processing logic. 

If you need to add a new method, just create a file here and call it from _method_launcher.py_

**core/models**

This is where model operations are allocated. All data operations are based on Pandas DataFrames NOT from ORM data.

File Suffixes:
- _filter_: functions used to filter data
- _helper_: util operations for model data
- _properties_: model data properties definitions. ie: function that determine if interaction is cellphonedb interactor.

**core/queries**

This is where are implemented the CellPhoneDB Queries. Queries are database interrogations with only data presentation logic. If you need to create a query with more data processing logic, please, create a method.

If you need to add a new query, just create a script inside and call it from _query_launcher.py_

**core/tests**

Contains the core unittests used to validate the business logic of the core

**core/utils/filters**

This is where are implemented some filters that are not associated to a model.


**core/cellphone.db**

CellPhoneDB SQLite database. This is where CellPhoneDB data is stored by default. It contain the last CellPhoneDB data version.

**core/Cellphonedb.py**

CellPhoneDB base core manager

**core/CellphonedbSqlalchemy.py**

CellPhoneDB SqlAlchemy core manager. This is the implementation using SqlAlchemy ORM

**core/core_logger.py**

Logging implementation for core logs.


**local_launchers**

Are the action bridges between flask terminal api and the CellPhoneDB core.

**tests** 

Cheks if the APIs, the app initialization and the current data are valid.


## tools

Here are allocated the tools to recreate and update the CellPhoneDB data lists. The code runs independently to cellphonedb scripts.

**actions**

This is where are allocated the actions called from the tools.py

**data**

This is where are allocated the input data (from external Databases and base CellPhoneDB data).

**generate_data**

Here are allocated the scripts to generate the CellPhoneDB lists from data files.

They are separated in 
- filters: for filtering functions
- getters: for functions that gets data from other API
- mergers: for functions to merge data from multiple lists
- parsers: here are allocated the functions that parse the raw lists from external data.

**out**

Here are allocated the result files after generate lists

**validators** 

Contains functions to validate generated lists

**app.py**

Flask app to enable terminal API

**interactions_helper.py**

Util functions for interactions

**merge_duplicated_proteins.py**

Util to merge correctly multiple proteins

**tools_helper.py**

Some common functions used in tools.


## Other folders

**Docs**

Allocates the CellPhoneDB documentation in markdown.

**in**

Default input folder for CellPhoneDB Terminal API methods

**out**

Default output folder for

**utils**

Contain some util functions to process dataframes, and generate ids.
  



