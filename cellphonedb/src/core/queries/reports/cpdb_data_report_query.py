def call(complex_compositions, interactions, proteins):
    report = {}
    interactions_cpdb = interactions[interactions['is_cellphonedb_interactor']]
    multidata_id_in_interactions_cpdb = interactions_cpdb['multidata_1_id'].append(
        interactions_cpdb['multidata_2_id']).drop_duplicates().tolist()
    protein_id_in_complex = complex_compositions['protein_multidata_id'].drop_duplicates().tolist()
    report['total_proteins'] = len(proteins)
    secreted_proteins = proteins[proteins['secretion']]
    report['secreted_proteins'] = len(secreted_proteins)
    secreted_proteins_incpdb_interaction = secreted_proteins[
        secreted_proteins['id_protein'].apply(lambda id: id in multidata_id_in_interactions_cpdb)]
    report['secreted_proteins_in_cpdb_interaction'] = len(secreted_proteins_incpdb_interaction)

    report['secreted_proteins_with_tag_to_add'] = len(secreted_proteins[secreted_proteins['tags'] == 'To_add'])
    report['secreted_proteins_with_tag_to_add_and_cpdb_interaction'] = len(
        secreted_proteins_incpdb_interaction[secreted_proteins_incpdb_interaction['tags'] == 'To_add'])

    transmembrane_proteins = proteins[proteins['transmembrane']]
    report['transmembrane_proteins'] = len(transmembrane_proteins)
    transmembrane_proteins_in_cpdb_interaction = transmembrane_proteins[
        transmembrane_proteins['id_protein'].apply(lambda id: id in multidata_id_in_interactions_cpdb)]
    report['transmembrane_proteins_in_cpdb'] = len(transmembrane_proteins_in_cpdb_interaction)

    report['transmembrane_proteins_with_tag_to_add'] = len(
        transmembrane_proteins[transmembrane_proteins['tags'] == 'To_add'])
    report['transmembrane_proteins_with_tag_to_add_and_cpdb_interaction'] = len(
        transmembrane_proteins_in_cpdb_interaction[transmembrane_proteins_in_cpdb_interaction['tags'] == 'To_add'])

    report['proteins_in_complex'] = len(protein_id_in_complex)
    proteins_in_cpdb_complex = complex_compositions[
        complex_compositions['complex_multidata_id'].apply(lambda id: id in multidata_id_in_interactions_cpdb)][
        'protein_multidata_id'].drop_duplicates().tolist()
    report['proteins_in_cpdb_complex'] = len(proteins_in_cpdb_complex)

    report['interactions'] = len(interactions)
    report['interactions_cpdb'] = len(interactions_cpdb)
    interactions_curated = interactions[interactions['source'] == 'curated']
    report['interactions_curated'] = len(interactions_curated.drop_duplicates())
    interactions_cpdb_curated = interactions_cpdb[interactions_cpdb['source'] == 'curated']
    report['interactions_curated_in_cpdb_interactions'] = len(interactions_cpdb_curated.drop_duplicates())
    interaction_duplicated = interactions_curated[
        interactions_curated['multidata_1_id'] == interactions_curated['multidata_2_id']]
    report['interaction_protein_duplicated'] = len(interaction_duplicated.drop_duplicates())
    interactions_iuphar = interactions[interactions['iuphar']]
    report['interactions_iuphar'] = len(interactions_iuphar.drop_duplicates())
    interactions_cpdb_iuphar = interactions_cpdb[interactions_cpdb['iuphar'] == True]
    report['interactions_cpdb_iuphar'] = len(interactions_cpdb_iuphar.drop_duplicates())
    interactions_non_curated_iuphar = interactions[
        (interactions['source'] != 'curated') & (interactions['iuphar'] == False)]
    report['interactions_non_curated_iuphar'] = len(interactions_non_curated_iuphar.drop_duplicates())
    interactions_cpdb_non_curated_iuphar = interactions_cpdb[
        (interactions_cpdb['source'] != 'curated') & (interactions_cpdb['iuphar'] == False)]
    report['interactions_cpdb_non_curated_iuphar'] = len(interactions_cpdb_non_curated_iuphar.drop_duplicates())
    return report
