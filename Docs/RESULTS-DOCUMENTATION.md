CELLPHONEDB TABLE GUIDE
============================================
Please, Check https://www.cellphonedb.org for more info


P-value (pvalues.txt), Mean (means.txt), Significant mean (significant_means.txt)
---------------------
* id_cp_interaction: Unique CellPhoneDB identifier for each interaction stored in the database.
* interacting_pair: Name of the interacting pairs separated by “|”.
* partner A or B: Identifier for the first interacting partner (A) or the second (B). It could be: UniProt (prefix `simple:`) or complex (prefix `complex:`)
* gene A or B: Gene identifier for the first interacting partner (A) or the second (B). The identifier will depend on the input user list.
* secreted: True if one of the partners is secreted.
* Receptor A or B: True if the first interacting partner (A) or the second (B) is annotated as a receptor in our database.
* annotation_strategy: Curated if the interaction was annotated by the CellPhoneDB developers. Otherwise, the name of the database where the interaction has been downloaded from.
* is_integrin: True if one of the partners is integrin.
* rank: Total number of significant p-values for each interaction divided by the number of cell type-cell type comparisons. (Only in significant_means.txt)
* means: Mean values for all the interacting partners: mean value refers to the total mean of the individual partner average expression values in the corresponding interacting pairs of cell types. If one of the mean values is 0, then the total mean is set to 0. (Only in mean.txt)
* p.values: p-values for the all the interacting partners: p.value refers to the enrichment of the interacting ligand-receptor pair in each of the interacting pairs of cell types. (Only in pvalues.txt)
* significant_mean: Significant mean calculation for all the interacting partners. If p.value < 0.05, the value will be the mean. Alternatively, the value is set to 0. (Only in significant_means.txt)

Importantly, the interactions are not symmetric. Partner A expression is considered on the first cluster, and partner B expression is considered on the second cluster. In other words:
* clusterA_clusterB = clusterA expressing partner A and clusterB expressing partner B.
* clusterA_clusterB and clusterB_clusterA  values will be different.


Deconvoluted (deconvoluted.txt)
-------------------------------
* gene_name: Gene identifier for one of the subunits that are participating in the interaction defined in “means.csv” file. The identifier will depend on the input of the user list.
* uniprot: UniProt identifier for one of the subunits that are participating in the interaction defined in “means.csv” file.
* is_complex: True if the subunit is part of a complex. Single if it is not, complex if it is.
* protein_name: Protein name for one of the subunits that are participating in the interaction defined in “means.csv” file.
* complex_name: Complex name if the subunit is part of a complex. Empty if not.
* id_cp_interaction: Unique CellPhoneDB identifier for each of the interactions stored in the database.
* mean: Mean expression of the corresponding gene in each cluster.
