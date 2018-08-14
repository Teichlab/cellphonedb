# CellPhoneDB  manager doc for Windows Systems

## Installing
0. **Requisites**:
- [Python3.5](https://www.python.org/downloads/release/python-366/)
- [Microsoft Build Tools 2015] (https://visualstudio.microsoft.com/vs/older-downloads/) (You can get it at the end of the page)

**IMPORTANT**:
If you have installed newer Microsoft Build Tools versions, you can have problems during installing process.


1. **Download** CellPhoneDB-0.0.6.tar.gz.

2. Go to the directory where CellPhoneDB-0.0.6.tar.gz is stored (**ie**: _%userprofile%/Downloads_ folder) & **unpack** CellPhoneDB manager (CellPhoneDB-0.0.6.tar.gz) using Winrar/7z or other software

3. Go to unpacked folder and install CellPhoneDB:

```
cd %userprofile%/Downloads/CellPhoneDB-0.0.6
python setup.py install
```


## Run Methods
0. In Command Prompt, go to Installation folder (ie. ~/Downloads/CellPhoneDB-0.0.6/) and set flask app variable

Code:
```
cd %userprofile%/Downloads/CellphoneDB-0.0.6
set FLASK_APP=manage.py
```


1. [Example] **Execute method with example data**.
Basic usage
Code:
```
flask method cluster_statistical_analysis example_data/test_meta.txt example_data/test_counts.txt
```

2. **Running your inputs**
Input files (meta and counts) shoud be allocated in  folder is found in CellPhoneDB-0.0.6
Files format: **.txt/.tsv/.tab** for tab separated format or **.csv** for comma separated format.


Results will be saved in  folder in .csv format.

Code:
```shell
flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt
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
flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt --project-name=new_project
```

Set output path
```shell
mkdir custom_folder
flask method cluster_statistical_analysis yourmetafile.txt yourcountsfile.txt --output-path=custom_folder
```