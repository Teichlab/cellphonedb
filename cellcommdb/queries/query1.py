import pandas as pd

from cellcommdb.extensions import db
from cellcommdb.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellcommdb.models.gene.db_model_gene import Gene
from cellcommdb.models.multidata.db_model_multidata import Multidata
from cellcommdb.models.protein.db_model_protein import Protein
from cellcommdb.tools import filters


class Query1:
    @staticmethod
    def call(processed_data):
        gene_protein_query = db.session.query(Gene.ensembl, Multidata.id).join(Protein).join(Multidata)
        gene_multidata = pd.read_sql(gene_protein_query.statement, db.engine)

        multidata_query = db.session.query(Multidata.id, Multidata.name)
        multidata_df = pd.read_sql(multidata_query.statement, db.engine)

        complex_composition_query = db.session.query(ComplexComposition)
        complex_composition_df = pd.read_sql(complex_composition_query.statement, db.engine)

        # Get complex genes
        cc_proteins = pd.merge(complex_composition_df, gene_multidata, left_on='protein_multidata_id', right_on='id',
                               how='outer', indicator=True)
        complex_genes = cc_proteins[cc_proteins['_merge'] == 'both']
        non_complex_genes = cc_proteins[cc_proteins['_merge'] == 'right_only']

        processed_non_complex_genes = pd.merge(non_complex_genes, processed_data, left_on='ensembl', right_on='gene')

        processed_complex_genes = pd.merge(complex_genes, processed_data, left_on='ensembl', right_on='gene')

        # TODO: move to query 0
        processed = pd.DataFrame()
        for index, processed_complex_gene in processed_complex_genes.iterrows():
            genes_complex_procesed_for_one_complex = processed_complex_genes[
                processed_complex_genes['complex_multidata_id'] == processed_complex_gene[
                    'complex_multidata_id']]
            genes_complex_composition_for_one_complex = complex_composition_df[
                complex_composition_df['complex_multidata_id'] == processed_complex_gene[
                    'complex_multidata_id']]
            if len(genes_complex_procesed_for_one_complex) == len(genes_complex_composition_for_one_complex):
                processed = processed.append(processed_complex_gene)

        processed = pd.merge(processed, multidata_df, left_on='complex_multidata_id', right_on='id')

        filters.remove_not_defined_columns(processed, ['name'] + list(processed_data.columns.values))

        processed.rename(index=str, columns={'name': 'complex_name'}, inplace=True)

        processed_unique = processed[processed.duplicated('complex_name') == False]

        cluster_names = list(processed_data.columns.values)
        del cluster_names[cluster_names.index('gene')]

        def merge_complex_processed(row):

            for cluster_name in cluster_names:
                if (processed[processed['complex_name'] == row['complex_name']][cluster_name].all()):
                    row[cluster_name] = processed[processed['complex_name'] == row['complex_name']][cluster_name].max()

                else:
                    row[cluster_name] = 0

            return row

        processed_unique = processed_unique.apply(merge_complex_processed, axis=1)

        def all_clusters_null(row):
            if row[cluster_names].any():
                return True

            return False

        processed_unique = processed_unique[processed_unique.apply(all_clusters_null, axis=1)]
        processed_unique.drop('gene', axis=1, inplace=True)

        filters.remove_not_defined_columns(processed_non_complex_genes, list(processed_data.columns.values))

        processed_unique['type'] = 'complex'
        processed_non_complex_genes['type'] = 'uniprot'
        processed_unique_and_noncomplex = processed_unique.append(processed_non_complex_genes)

        return processed_unique_and_noncomplex
