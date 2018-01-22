import os

import pandas as pd
from cellphonedb.api import current_dir
from cellphonedb.blend import Blend
from cellphonedb.extensions import db
from cellphonedb.models.gene.db_model_gene import Gene
from cellphonedb.tools import filters, database


def load(gene_file=None):
    """
    Loads gene table from csv.
    - Load human gene data
    :param gene_file:
    :return:
    """

    if not gene_file:
        gene_file = os.path.join(current_dir, 'data', 'gene.csv')

    csv_gene_df = pd.read_csv(gene_file)

    gene_df = Blend.blend_protein(csv_gene_df, ['uniprot'])

    gene_df.rename(index=str, columns={'uniprot': 'name'},
                   inplace=True)

    filters.remove_not_defined_columns(gene_df, database.get_column_table_names(Gene, db))

    gene_df.to_sql(name='gene', if_exists='append', con=db.engine, index=False)
