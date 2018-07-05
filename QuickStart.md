# CellPhoneDB  manager doc

## First time
0. **Requisites**:
- Python3
- Pip3
- python3-venv



1. **Download** CellPhoneDB-0.0.3.tar.gz.

2. Go to the directory where CellPhoneDB-0.0.3.tar.gz is stored (**ie**: _~/Downloads_ folder) & **unpack** CellPhoneDB manager (CellPhoneDB-0.0.3.tar.gz).

Code:
```shell
cd ~/Downloads
tar -xzf CellPhoneDB-0.0.3.tar.gz
cd CellPhoneDB-0.0.3
```

3. **Create Virual Env**.

Code:
```shell
python3 -m venv cpdb-env &&
source cpdb-env/bin/activate &&
python setup.py install
```


## Run Methods
0. You need to activate the Virtual Env (if is the first time or you closed the terminal)

```shell
source cpdb-env/bin/activate
```


1. [Example] **Execute method with example data**.

Basic usage
Code:
```shell
FLASK_APP=manage.py flask method cluster_statistical_analysis example_data/test_meta.txt example_data/test_counts.txt
```

2. **Running your inputs**
Input files (meta and counts) shoud be allocated in  folder is found in CellPhoneDB-0.0.3
Files format: **.txt/.tsv/.tab** for tab separated format or **.csv** for comma separated format.


Results will be saved in  folder in .csv format.

Code:
```shell
FLASK_APP=manage.py flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt
```


~ **Optional parameters**:
`--project-name`: Name of the project. It creates a subfolder in output folder
`--iterations`: Number of pvalues analysis iterations [1000]
`--data-path`: Directory where is allocated input data [in]
`--output-path`: Directory where the results will be allocated (the directory must exist) [out]
`--means-result-name`: Means result namefile [means.txt]
`--pvalues-result-name`: Pvalues result namefile [pvalues.txt]
`--significant-mean-result-name`: Significant result namefile [significant_means.txt]
`--means-pvalues-result-name`: Pvalues-means result namefile [pvalues_means.txt]
`--deconvoluted-result-name`: Deconvoluted result namefile [deconvoluted.txt]
`--debug-seed`: Debug random seed 0 for disable it. >=0 to set it [-1]

**Usage Examples**:

Set project subfolder
```shell
FLASK_APP=manage.py flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt --project-name=new_project
```

Set output path
```shell
mkdir custom_folder
FLASK_APP=manage.py flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt --output-path=custom_folder
```