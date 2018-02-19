import pandas as pd
from flask_testing import TestCase

from cellphonedb import extensions
from cellphonedb.api import create_app
from cellphonedb.core.models.gene.db_model_gene import Gene
from cellphonedb.core.models.multidata.db_model_multidata import Multidata
from cellphonedb.core.models.protein.db_model_protein import Protein

KNOWED_PROTEINS_WITHOUT_GENE = ['Q5VU13', 'P48960', 'Q30KQ2', 'Q6UXV3', 'Q8WXG9', 'Q9BZG9', 'P01782', 'A8MVG2',
                                'Q8NGJ3', 'P0C617',
                                'P0C7N5', 'O42043', 'O71037', 'P61565', 'P61566', 'Q69384', 'Q902F8', 'Q9UKH3',
                                'Q902F9', 'A6NIZ1',
                                'P60507', 'P87889', 'Q9YNA8', 'P62683', 'P63145', 'P61570', 'Q9HDB9', 'Q7LDI9',
                                'P61567', 'P63130',
                                'P62685', 'P63126', 'P63128', 'P60509', 'P61550', 'P62684', 'Q9N2J8', 'Q9N2K0',
                                'P04435', 'A6NKC4',
                                'Q4G0T1', 'A6NJS3', 'A6NJ16', 'Q96I85', 'Q5TEV5', 'Q96LR1', 'Q71RG6', 'Q6IE37',
                                'Q6IE36', 'Q9P1C3',
                                'A8MTI9', 'Q6UY13', 'A8MTW9', 'A8MUN3', 'Q6ZRU5', 'Q6UXQ8', 'Q6UXR6', 'Q6UXU0',
                                'Q13072', 'Q86Y29',
                                'Q86Y28', 'Q86Y27', 'HLAF', 'HLAA', 'HLADRA', 'HLADRB5', 'HLADRB1', 'HLADQA1',
                                'HLADQB1', 'HLADQA2',
                                'HLADQB2', 'HLADOB', 'HLAC', 'HLAB', 'HLADMB', 'HLADMA', 'HLADOA', 'HLADPA1', 'HLADPB1']


class DatabaseRelationsChecks(TestCase):
    def test_all_protein_have_gen(self):

        expected_protein_without_gene = 159
        protein_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Protein,
                                                                                                         Multidata.name).join(
            Multidata)

        protein_df = pd.read_sql(protein_query.statement,
                                 extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)
        protein_ids = protein_df['id_protein'].tolist()

        gene_query = extensions.cellphonedb_flask.cellphonedb.database_manager.database.session.query(Gene.protein_id)
        gene_protein_ids = \
        pd.read_sql(gene_query.statement, extensions.cellphonedb_flask.cellphonedb.database_manager.database.engine)[
            'protein_id'].tolist()

        protein_without_gene = []
        for protein_id in protein_ids:
            if not protein_id in gene_protein_ids:
                protein_without_gene.append(protein_df[protein_df['id_protein'] == protein_id]['name'].iloc[0])

        if len(protein_without_gene) != expected_protein_without_gene:
            print('There are {} Proteins without gene'.format(len(protein_without_gene)))
            print(protein_without_gene)

            unknowed_proteins_without_gene = []
            for protein in protein_without_gene:
                if not protein in KNOWED_PROTEINS_WITHOUT_GENE:
                    unknowed_proteins_without_gene.append(protein)

            if unknowed_proteins_without_gene:
                print('There are {} unowed proteins without gene'.format(len(unknowed_proteins_without_gene)))
                print(unknowed_proteins_without_gene)

        self.assertEqual(len(protein_without_gene), expected_protein_without_gene, 'There are Proteins without Gene.')

    def create_app(self):
        return create_app()
