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
- `--output-format`: Result files output format (extension will be added to filename if not present) [txt]
- `--means-result-name`: Means result filename [means]
- `--significant-means-result-name`: Significant result filename [significant_means]
- `--deconvoluted-result-name`: Deconvoluted result filename [deconvoluted]
- `--verbose/--quiet`: Print or hide cellphonedb logs [verbose]
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
- `--verbose / --quiet`: Print or hide cellphonedb logs [verbose]

Available output formats are those supported by `R's ggplot2` package, among others tey are:
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
- `--meta-path`: Analysis input meta file [meta.txt]
- `--pvalues-path`: Analysis output pvalues [./out/pvalues.txt]
- `--output-path`: Path to write generated plots [./out]
- `--count-name`: Analysis output pvalues [heatmap_count.pdf]
- `--log-name`: Analysis output pvalues [heatmap_log_count.pdf]
- `--verbose / --quiet`: Print or hide cellphonedb logs [verbose]

Available output formats are those supported by `R's pheatmap` package, among others tey are:
- `pdf`
- `png`
- `jpeg`

This format will be inferred from the `--count-name` & `--log-name` argument


## Contributing to CellPhoneDB

CellPhoneDB is Open Source project. If you are interesed to contribute to this project, please let us know.


You can check all project documentation in [Docs](Docs) section
