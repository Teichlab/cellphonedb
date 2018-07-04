# CellPhoneDB  manager doc

## First time
0. **Requisites**:
- Python3
- Pip3
- python3-venv



1. **Download** CellPhoneDB-0.0.2.tar.gz.

2. Go to the directory where CellPhoneDB-0.0.1.tar.gz is stored (**ie**: _~/Downloads_ folder) & **unpack** CellPhoneDB manager (CellPhoneDB-0.0.1.tar.gz).

Code:
```shell
cd ~/Downloads
tar -xzf CellPhoneDB-0.0.2.tar.gz
cd CellPhoneDB-0.0.2
```

3. **Create Virual Env**.

Code:
```shell
python3 -m venv cpdb-env &&
source cpdb-env/bin/activate &&
python setup.py install
```


## Run Queries
0. You need to activate the Virtual Env (if is the first time or you closed the terminal)

```shell
source cpdb-env/bin/activate
```


1. [Example] **Execute method with example data**.

Code:
```shell
FLASK_APP=manage.py flask call_query cluster_statistical_analysis example_data/test_meta.txt example_data/test_counts.txt
```

2. **Running your inputs**
Input files (meta and counts) shoud be allocated in 'in' folder. 'in' folder is found in CellPhoneDB-0.0.1
Files format: **.txt/.tsv** for tab separated format or **.csv** for comma separated format.


Results will be saved in 'out' folder in .csv format.

Code:
```shell
FLASK_APP=manage.py flask call_query cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt
```


~ **Optional parameters** (are cumulative):
- iterations (1000): number of iterations for statistical script
- data_path (empty): if you need to change the data path
- output_path (empty): if you need to change the results path
- means_result_filename (means.txt): result filename for means data
- pvalues_result_filename (pvalues.txt): result filename for pvalues data
- significant_mean_result_filename (significant_means.txt): result filename for significant means data
- means_pvalues_result_filename ('pvalues_means.txt'): result filename for pvalues_means data
- deconvoluted_result_filename ('deconvoluted.txt'): result filename for deconvoluted
- debug_seed (0): set the seed of rand generate data (for debug proposals)