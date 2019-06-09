# Create Datafiles
CellPhoneDB base data is based on other biologic databases.
You can use **tools scripts** to update/recreate CellPhoneDB base data.
When you finish to generate all data, please copy it in cellphonedb/code/data path and run collect script to update the database    

## Database input files
CellPhoneDB database needs this input tables:
1. **complex.csv**
2. **gene.csv**
3. **interaction.csv**
4. **protein.csv**

The order is important because they have data dependences.

## Using tools.py
Tools.py is the provided tool to preprocesate the CellPhoneDB database input data.

Result data is saved in out tools/out path and input data is allocated in tools/data path. 

### Recreating gene.csv
**gene.csv** data is based on [Ensembl database](https://www.ensembl.org/) and [Uniprot database](https://www.uniprot.org). This data files needs to be downloaded from source page
In addition, you need to provide:

- _protein.csv_: CellPhoneDB protein list (to filter only the genes associated to CellPhoneDB proteins).
- _remove_genes.csv_: Gene list needed to remove duplicated ensembls from imported data.
- _hla_curated.csv_: HLA Gene list to attach to the input data


#### Steps:
1. Merge Ensembl database and Uniprot on gene_name
2. Add HLA genes
3. Remove genes from list and make some checks to validate the final result

#### Command:
```shell
python3 tools.py generate_genes uniprot_db_filename ensembl_db_filename proteins_filename remove_genes_filename hla_genes_filename [--result_filename] [--result_path] [--gene_uniprot_ensembl_merged_result_filename] [--add_hla_result_filename]
```


#### Execution example: 
 ```shell
python3 tools.py generate_genes uniprot-filtered-organism_20180625.tab ensembl_db_20180625.txt ../../cellphonedb/core/data/protein.csv genes_to_remove_20180701.csv hla_genes_20180100.txt
 ```

***Results***:
generate_genes script creates multiple files in output dir:
- _gene_uniprot_ensembl_merged.csv_ is the result of merge uniprot and ensembl databases.
- _gene_hla_added.csv_ is the result of add hla genes to _gene_uniprot_ensembl_merged.csv_ list
- _gene.csv_ is the final result (ready to be used in CellPhoneDB collector) after remove some provided genes.



### Recreating interaction.csv
**interaction.csv** is based on [Imex database](https://www.imexconsortium.org/), [Guide To Pharmacology database](http://www.guidetopharmacology.org/download.jsp).

In adition, you need to provide:

- _protein.csv_: CellPhoneDB protein list.
- _gene.csv_: CellPhoneDB gene list.
- _complex.csv_: CellPhoneDB complex list.
- _remove_interactions.csv_: List of interactions to remove

#### Steps:
1. Process Imex raw interactions
2. Get Iuphar raw database (check if new version is available)
3. Process Iuphar interactions
4. Merge ensemble/iuphar interactions
5. Remove Complex interactions
6. Remove provided interactions
7. Add curated interactions


 imex_raw_filename: str,
iuphar_raw_filename: str,
        database_proteins_filename: str,
        database_gene_filename: str,
        database_complex_filename: str,
        interaction_to_remove_filename: str,
        interaction_curated_filename: str

#### Command:
```shell
python3 tools.py generate_interactions imex_raw_filename iuphar_raw_filename proteins_filename gene_filename complex_filename remove_interactions_filename interactions_curated_filename
```

#### Execution example:
```shell
python3 tools.py generate_interactions interactionsMirjana.txt interaction_iuphar_guidetopharmacology__20180619.csv ../../cellphonedb/core/data/protein.csv ../../cellphonedb/core/data/gene.csv ../../cellphonedb/core/data/complex.csv remove_interactions_20180330.csv interaction_curated_20180729.csv
```

## Loading the new data in CellPhoneDB 

Once the data is builded, you need to move the `interaction.csv` file and the `gene.csv` file from `tools/out` folder to
`cellphonedb/core/data` replacing the old files. 

Aftewards, please upgrade the database using the following code:

```
FLASK_APP=manage.py flask reset_db
FLASK_APP=manage.py flask collect all 
```

This commands removes the actual database (allocated by default in `cellphonedb/code/cellphone.db` using sqlite) and 
creates the new one with the updated data.