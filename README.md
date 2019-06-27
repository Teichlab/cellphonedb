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

3. Install CellPhoneDB
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
- `--output-format`: Result files output format (extension will be added to filename if not present) [txt]
- `--means-result-name`: Means result filename [means]
- `--significant-means-result-name`: Significant result filename [significant_means]
- `--deconvoluted-result-name`: Deconvoluted result filename [deconvoluted]
- `--verbose/--quiet`: Print or hide CellPhoneDB logs [verbose]
- `--subsampling`: Enable Cells subsampling
- `--subsampling-log`: Enable subsampling log1p for non transformed data inputs !!mandatory!!
- `--subsampling-num-pc`: Subsampling NumPC argument [100]
- `--subsampling-num-cells`: Number of cells to subsample [1/3 of cells]


~ **Optional Method Statistical parameters**
- `--pvalues-result-name`: Pvalues result filename [pvalues]
- `--pvalue`: Pvalue threshold [0.05]
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

Subsampling
```shell
cellphonedb method analysis yourmetafile.txt yourcountsfile.txt --subsampling --subsampling-log false --subsampling-num-cells 3000
```

## Plotting statistical method results

In order to plot results from statistical methods you need to run it first.

Currently there are two plot types available `dot_plot` & `heatmap_plot`

Once you have the needed files (`means` & `pvalues`) you can proceed as follows:
```shell
cellphonedb plot dot_plot
```

```shell
cellphonedb plot heatmap_plot yourmeta.txt
```

### `dot_pot`
This plot type requires `ggplot2` R package installed and working

You can tweak the options for the plot with these arguments:
- `--means-path`: Analysis output means [./out/means.txt]
- `--pvalues-path`: Analysis output pvalues [./out/pvalues.txt]
- `--output-path`: Path to write generated plot [./out]
- `--output-name`: Output file with plot [plot.pdf]
- `--rows`: File with a list of rows to plot, one per line [all available]
- `--columns`: File with a list of columns to plot, one per line [all available]
- `--verbose / --quiet`: Print or hide CellPhoneDB logs [verbose]

Available output formats are those supported by `R's ggplot2` package, among others they are:
- `pdf`
- `png`
- `jpeg`

This format will be inferred from the `--output-name` argument

To plot only desired rows/columns (samples for [rows](in/example_data/rows.txt) and [columns](in/example_data/columns.txt) based in example data files) :
```shell
cellphonedb plot dot_plot --rows in/rows.txt --columns in/columns.txt
``` 

### `heatmap_plot`
This plot type requires `pheatmap` R package installed and working 
This plot type includes to plots: `count` & `log_count` 

You can tweak the options for the plot with these arguments:
- `--pvalues-path`: Analysis output pvalues [./out/pvalues.txt]
- `--output-path`: Path to write generated plots [./out]
- `--count-name`: Analysis output pvalues [heatmap_count.pdf]
- `--pvalue`: pvalue threshold to consider when plotting [0.05]
- `--log-name`: Analysis output pvalues [heatmap_log_count.pdf]
- `--verbose / --quiet`: Print or hide cellphonedb logs [verbose]

Available output formats are those supported by `R's pheatmap` package, among others they are:
- `pdf`
- `png`
- `jpeg`

This format will be inferred from the `--count-name` & `--log-name` argument


## Using different database versions
CellPhoneDB databases can be updated from remote repository through our tool. Available versions can be listed and downloaded to be used.

To use one of those versions a user must provide the `--database <version_or_file>` to the method to be executed.

If the given parameter is a readable database file it will be used as is. Otherwise it will use some of the versions matching the selected version.


If the selected version does not exist in the local environment it will be downloaded from the remote repository. (See below)
If no `--database` argument is given in methods execution it will use the latest local version available.

Downloaded versions will be stored in a user folder under `~/.cpdb/releases`

## Listing remote available versions
The command to list available versions from the remote repository is:
```shell
cellphonedb database list_remote
``` 

## Listing local available versions
The command to list available versions from the remote repository is:
```shell
cellphonedb database list_local
``` 

## Download version
The command to download a version from the remote repository is:
```shell
cellphonedb database download
``` 
or 

```shell 
cellphonedb database download --version <version_spec|latest> 
``` 

`version_spec` must be one of the listed in the `database list_remote` command.
If no version is specified or `latest` is used as a `version_spec` the newest available version will be downloaded


## Generating User database
A user can generate custom databases and use them. In order to generate a new database a user can provide his/her own lists.

These lists can be: genes, proteins, complexes and/or interactions. In the generation process they will get merged with the ones from
the CellPhoneDB release sources. The user lists have higher precedence than the ones included in CellPhoneDB package.

To generate such a database the user has to issue this command:
```shell
cellphonedb database generate  
```

Result database file is generated in `out` with `cellphonedb_user_{datetime}.db`. To use this database, please use `--database` parameter in methods.
E.g:
```
 cellphonedb method statistical_analysis in/example_data/test_meta.txt in/example_data/test_counts.txt --database out/cellphonedb_user_2019-05-10-11_10.db
```

Some lists can be downloaded from original sources while creating the database, eg: uniprot, ensembl. By the default the snapshots included in
the CellPhoneDB package will be used, to enable a fresh copy `--fetch` must be appended to the command.

In order to use specific lists those can be specified like this `--user-protein`, `--user-gene`, `--user-complex`, `--user-interactions`,
followed by the corresponding file path.

The database file can be then used as explained below. The intrermediate lists used for the generation will be saved along the database itself.
As the lists as processed, then filtered, and lastly collected, two versions may exist: `_generated` is the unfiltered one 
whereas `_input` is the final state prior being inserted in the database.

Generating individually lists is considered advanced it is disabled by default, to enable it an `ADVANCED` environment variable must be set to any value in the running shell.  


## Using different database versions
CellPhoneDB databases can be updated from remote repository through our tool. Available versions can be listed and downloaded to be used.

To use one of those versions a user must provide the `--database <version_or_file>` to the method to be executed.

If the given parameter is a readable database file it will be used as is. Otherwise it will use some of the versions matching the selected version.


If the selected version does not exist in the local environment it will be downloaded from the remote repository. (See below)
If no `--database` argument is given in methods execution it will use the latest local version available.

Downloaded versions will be stored in a user folder under `~/.cpdb/releases`

## Listing remote available versions
The command to list available versions from the remote repository is:
```shell
cellphonedb database list_remote
``` 

## Listing local available versions
The command to list available versions from the remote repository is:
```shell
cellphonedb database list_local
``` 

## Download version
The command to download a version from the remote repository is:
```shell
cellphonedb database download
``` 
or 

```shell 
cellphonedb database download --version <version_spec|latest> 
``` 

`version_spec` must be one of the listed in the `database list_remote` command.
If no version is specified or `latest` is used as a `version_spec` the newest available version will be downloaded


## Generating Custom database
A user can generate custom databases and use them (See advanced documentation regarding this issue) 



## Contributing to CellPhoneDB

CellPhoneDB is Open Source project. If you are interesed to contribute to this project, please let us know.


You can check all project documentation in [Docs](Docs) section
