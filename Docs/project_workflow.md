# CellPhoneDB Project Workflow
CellPhoneDB is developed using multiple libraries and frameworks.

The project is designed to isolate library dependencies as much as possible. This makes it easier to change the libraries in the future.

This is the structure of the project modules/layers:

![alt text](images/project_workflow.png "Logo Title Text 1")

## Web Page Layer
This is an independent project developed in PHP. It enables a web portal to make requests and visualize results of CellPhoneDB.

The web application communicates to the server over the Flask Web http API allocated in API Layer.

## Terminal Layer  
This is the user server communication portal. It enables some commands to make methods, queries, export data and update data.

It communicates with the Flask Terminal API in API Layer

## API Layer
The API Layer is developed in [Flask](http://flask.pocoo.org/) and enables a http (using [Flask-RESTful extension](https://flask-restful.readthedocs.io/en/latest/)) and terminal API (using  [Click Flask package](http://click.pocoo.org/5/)) to communicate with the outside.

## Local Layer
This is used to read/write input/output files in the system. It is necessary to isolate the Flask Terminal API and Core Layer during the loading/finishing processes.

## Business Logic Layer
This is where all CellPhoneDB Business Logic is allocated. It does not have dependencies with the flask/SqlAlchemy libraries and it can be executed without load the previous layers. In the future, we will create a package to import CellPhonDB directly from other Python packages.

## Database Layer
This is where the database communications are done. Is developed using [SQLAlchemy](https://www.sqlalchemy.org/) and it isolates the ORM dependence. Outside of this layer, all data is processed using [Pandas library](https://pandas.pydata.org/) data structures.
