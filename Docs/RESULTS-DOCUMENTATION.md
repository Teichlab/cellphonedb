# Documents for the user:
## Document 1: p-value (pvalues.csv)
* **Id_cp_interaction**: CellPhoneDB interaction id
* **Interacting_pair**: Intercating pairs
* **Partner A**: Uniprot id for the first interacting partner
* **Partner B**: Uniprot id for the second interacting partner
* **Ensembl A**: Ensembl id for the first interacting partner
* **Ensembl B**: Ensembl id for the second interacting partner
* **Secreted**: True if one of the partners is secreted.
* **Stoichiometry**: i) single- homodimer; ii) complex- heterodimer
* **Source**: i) curated- interaction annotated by CellPhoneDB developers; ii) iuphar- interaction annotated by IUPHAR consortium; iii) iMEX- interaction annotated by iMEX consortium.
* **Is.integrin**: True if the interaction is an integrin.
* **P.values for the all the interacting partners**: The p.value referees to the enrichment of the interacting ligand/receptor pair in each of the interacting pair of cells.


**Importantly**, the interactions are not symmetric. Partner A expression is considered on the first cluster, and partner B expression is considered on the second cluster. In other words:
- clusterA_clusterB = clusterA expressing partner A and clusterB expressing partner B.
- clusterA_clusterB and clusterB_clusterA  values will be different.

## Document 2: mean (mean.csv)
* **Id_cp_interaction**: CellPhoneDB interaction id
* **Interacting_pair**: Intercating pairs
* **Partner A**: Uniprot id for the first interacting partner
* **Partner B**: Uniprot id for the second interacting partner
* **Ensembl A**: Ensembl id for the first interacting partner
* **Ensembl B**: Ensembl id for the second interacting partner
* **Secreted**: True if one of the partners is secreted.
* **Stoichiometry**: i) single- homodimer; ii) complex- heterodimer
* **Source**: i) curated- interaction annotated by CellPhoneDB developers; ii) iuphar- interaction annotated by IUPHAR consortium; iii) iMEX- interaction annotated by iMEX consortium.
* **Is.integrin**: True if the interaction is an integrin.
* **Mean calculation for all the interacting partners**: Mean value referees to the sum of the individual partner means. If one of the expression values is 0, then the total mean will be 0.

**Importantly**, the interactions are not symmetric. Partner A expression is considered on the first cluster, and partner B expression is considered on the second cluster. In other words:
* clusterA_clusterB = clusterA expressing partner A and clusterB expressing partner B.
* clusterA_clusterB and clusterB_clusterA  values will be different.

## Document 3: significant mean. (significant_mean.csv)
* **Id_cp_interaction**: CellPhoneDB interaction id
* **Interacting_pair**: Intercating pairs
* **Partner A**: Uniprot id for the first interacting partner
* **Partner B**: Uniprot id for the second interacting partner
* **Ensembl A**: Ensembl id for the first interacting partner
* **Ensembl B**: Ensembl id for the second interacting partner
* **Secreted**: True if one of the partners is secreted.
* **Stoichiometry**: i) single- homodimer; ii) complex- heterodimer
* **Source**: i) curated- interaction annotated by CellPhoneDB developers; ii) iuphar- interaction annotated by IUPHAR consortium; iii) iMEX- interaction annotated by iMEX consortium.
* **Is.integrin**: True if the interaction is an integrin.
* **Significant mean calculation for all the interacting partners**. If p.value < 0.05, the value will be the mean. Alternatively, the value would be equal to 0.


**Importantly**, the interactions are not symmetric. Partner A expression is considered on the first cluster, and partner B expression is considered on the second cluster. In other words:
* clusterA_clusterB = clusterA expressing partner A and clusterB expressing partner B.
* clusterA_clusterB and clusterB_clusterA  values will be different.

## Document 4: p.value_means (pvalues_means.csv)
* **Id_cp_interaction**: CellPhoneDB interaction id
* **Interacting_pair**: Intercating pairs
* **Partner A**: Uniprot id for the first interacting partner
* **Partner B**: Uniprot id for the second interacting partner
* **Ensembl A**: Ensembl id for the first interacting partner
* **Ensembl B**: Ensembl id for the second interacting partner
* **Secreted**: True if one of the partners is secreted.
* **Stoichiometry**: i) single- homodimer; ii) complex- heterodimer
* **Source**: i) curated- interaction annotated by CellPhoneDB developers; ii) iuphar- interaction annotated by IUPHAR consortium; iii) iMEX- interaction annotated by iMEX consortium.
* **Is.integrin**: True if the interaction is an integrin.
* **P.values and mean calculation for all the interacting partners**. Value in the same field, separated by “|”


**Importantly**, the interactions are not symmetric. Partner A expression is considered on the first cluster, and partner B expression is considered on the second cluster. In other words:
* clusterA_clusterB = clusterA expressing partner A and clusterB expressing partner B.
* clusterA_clusterB and clusterB_clusterA  values will be different.

## Document 5: deconvoluted (deconvoluted.csv)
* **entry_name**: molecule name
* **gene_name**: Ensembl id
* **name**: Uniprot id
* **is_complex**: i) single- homodimer; ii) complex- heterodimer
* **complex_name**: name of  the complex
* **Id_cp_interaction**: CellPhoneDB interaction id
* **values for each cluster**: Mean of the value.

