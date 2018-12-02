# CellPhoneDB

## What is CellPhoneDB?
CellPhoneDB is a publicly available repository of curated receptors, ligands and its interactions. Subunit architecture is included for both ligands and receptors, representing heteromeric complexes accurately. This is crucial, as cell-cell communication relies on multi-subunit protein complexes that go beyond the binary representation used in most databases and studies.

CellPhoneDB integrates [existing datasets](Docs/ppi-resources.md) that pertain to cellular communication and new manually reviewed information. Prestigious databases CellPhoneDB gets information are: UniProt, Ensembl, PDB, the IMEx consortium, IUPHAR.

CellPhoneDB can be used to search for a particular ligand/receptor or interrogate your own single-cell transcriptomics data.


## Starting to use CellPhoneDB 

To start using CellPhoneDB, you can use our interactive web ([cellphonedb.org](https://www.cellphonedb.org)) and run in the analysis in our private cloud, 
or just run CellPhoneDB in your computer/cloud/farm. Please, take the second way if you are going to work with big datasets).


### Installing CellPhoneDB
NOTE: Works with Python v3.5 or superior. If your default Python interpreter is for v2.x (you can check it with `python --version`), calls to `python`/`pip` should be substituted by `python3`/`pip3`.

We highly recommend to use a virtual env (steps 1 and 2) but you can omit.
1. Create python > 3.5 virtual-env
```shell
python -m venv cpdb-venv
```

2. Activate virtual-env
```shell
source cpdb-venv/bin/activate
```

3. Install cellphonedb
```shell
pip install cellphonedb
```


## Running CellPhoneDB Methods

Please, run step 0 if you didn't activate the virtual-env previously

0. Activate virtual-env
```shell
source cpdb-venv/bin/activate
```

For run example data, please [download meta/counts test data](https://github.com/Teichlab/cellphonedb/blob/master/in/example_data/cellphonedb_example_data.zip?raw=true).

Hint (if you are in terminal):
```shell
curl https://raw.githubusercontent.com/Teichlab/cellphonedb/master/in/example_data/test_counts.txt --output test_counts.txt
curl https://raw.githubusercontent.com/Teichlab/cellphonedb/master/in/example_data/test_meta.txt --output test_meta.txt
```

###  Example with running the statistical method
```shell
cellphonedb method statistical_analysis test_meta.txt test_counts.txt 
```


### Example without using the statistical method
```shell
cellphonedb method analysis test_meta.txt test_counts.txt 
```

Please check [result documentation](Docs/RESULTS-DOCUMENTATION.md) for underestand the results.

### Method optional parameters

~ **Optional Method parameters**:
- `--project-name`: Name of the project. It creates a subfolder in output folder
- `--iterations`: Number of pvalues analysis iterations [1000]
- `--threshold`: % of cells expressing a gene
- `--result-precision`: Number of decimal digits in results [3]
- `--output-path`: Directory where the results will be allocated (the directory must exist) [out]
- `--means-result-name`: Means result namefile [means.txt]
- `--significant-mean-result-name`: Significant result namefile [significant_means.txt]
- `--deconvoluted-result-name`: Deconvoluted result namefile [deconvoluted.txt]
- `--verbose/--quiet`: Print or hide cellphonedb logs [verbose]

~ **Optional Method Statistical parameters**
- `--pvalues-result-name`: Pvalues result namefile [pvalues.txt]
- `--means-pvalues-result-name`: Pvalues-means result namefile [pvalues_means.txt]
- `--debug-seed`: Debug random seed -1 for disable it. >=0 [-1]
- `--threads`: Number of threads to use. >=1 [-1]

**Usage Examples**:

Set number of iterations and threads
```shell
cellphonedb method statistical_analysis yourmetafile.txt yourcountsfile.txt --iterations=10 --threads=2
```
Set project subfolder
```shell
cellphonedb method analysis yourmetafile.txt yourcountsfile.txt --project-name=new_project
```

Set output path
```shell
mkdir custom_folder
cellphonedb method statistical_analysis yourmetafile.txt yourcountsfile.txt --output-path=custom_folder
```

## Contributing to CellPhoneDB

CellPhoneDB is Open Source project. If you are interesed to contribute to this project, please let us know.


You can check all project documentation in [Docs](Docs) section
