# CellPhoneDB  manager doc for Unix systems (Linux/macOS) for windows please check QuickStartWindows doc

## First time
0. **Requisites**:
- Python >= 3.5
- Pip3


1. [Example] **Execute method with example data**.

Basic usage
Code:
```shell
FLASK_APP=manage.py flask method cluster_statistical_analysis example_data/test_meta.txt example_data/test_counts.txt
```

2. **Running your inputs**
Input files (meta and counts) shoud be allocated in  folder is found in CellPhoneDB-0.0.6
Files format: **.txt/.tsv/.tab** for tab separated format or **.csv** for comma separated format.


Results will be saved in  folder in .csv format.

Code:
```shell
FLASK_APP=manage.py flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt
```


~ **Optional parameters**:
`--project-name`: Name of the project. It creates a subfolder in output folder
`--iterations`: Number of pvalues analysis iterations [1000]
`--threshold`: % of cells expressing a gene
`--data-path`: Directory where is allocated input data [in]
`--output-path`: Directory where the results will be allocated (the directory must exist) [out]
`--means-result-name`: Means result namefile [means.txt]
`--pvalues-result-name`: Pvalues result namefile [pvalues.txt]
`--significant-mean-result-name`: Significant result namefile [significant_means.txt]
`--means-pvalues-result-name`: Pvalues-means result namefile [pvalues_means.txt]
`--deconvoluted-result-name`: Deconvoluted result namefile [deconvoluted.txt]
`--debug-seed`: Debug random seed -1 for disable it. >=0 [-1]
`--threads`: Number of threads to use. >=1 [-1]

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