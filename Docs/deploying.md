# Deploy CellPhoneDB
Based on the python official documentation for [packaging python products](https://packaging.python.org/tutorials/packaging-projects/)

## Run CellPhoneDB from local package
Enables to run cellphonedb command from local source code.

```bash
# Create and mount new environment
python3 -m venv cpdb-venv
source cpdb-venv/bin/activate

# Install cellphonedb package from local source
pip install --editable .
```

## Deploy a new version of CellPhoneDB

Update the CellPhoneDB version editing version line in `setup.py`.

Make sure you have the latest versions of setuptools and wheel installed:
```shell
python -m pip install --user --upgrade setuptools wheel 
```

Create new package
```shell
python setup.py sdist bdist_wheel
```

This will create a CellPhoneDB package ready to be distributed in the `dist` folder, i.e.
```
dist/CellPhoneDB-0.0.5.tar.gz
```
