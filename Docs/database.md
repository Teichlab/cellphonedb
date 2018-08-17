# CellPhoneDB Database 
CellPhoneDB uses [SqlAlchemy](https://www.sqlalchemy.org/) for database schema connection. By default runs using sqllite connector and
his data is allocated in `cellphonedb/core/cellphone.db`.

## Cellphonedb Schema
This is the data schema:
![Database schema](images/database-schema.png "CellPhoneDB Database Schema")

**About Multidata table**

This saves the common info of proteins and complexes columns. That allows us to link interactions without need to check if is simple or complex data.