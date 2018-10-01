# Deploy CellPhoneDB
Based on [python official documentation](https://packaging.python.org/tutorials/packaging-projects/)


## Deploy a new version of CellPhoneDB

Update the CellPhoneDB version editing version line in setup.py.

Make sure you have the latest versions of setuptools and wheel installed:
```shell
python -m pip install --user --upgrade setuptools wheel
```

Create new package
```shell
python setup.py sdist bdist_wheel
```

This create a CellPhoneDB package ready to be distributed in dist folder.

ie:
```
dist/CellPhoneDB-0.0.5.tar.gz
```