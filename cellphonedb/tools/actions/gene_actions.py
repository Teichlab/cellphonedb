from cellphonedb.tools.generate_data.filters import remove_genes
from cellphonedb.tools.generate_data.mergers import mergers_genes
from cellphonedb.tools.validators import gene_validators
from cellphonedb.utils import utils


def remove_genes_in_file(gene_base_filename: str,
                         remove_genes_filename: str,
                         result_filename: str = 'gene_filtered.csv',
                         ) -> None:

    gene_base_data = utils.read_data_table_from_file(gene_base_filename)
    remove_genes_data = utils.read_data_table_from_file(remove_genes_filename)

    genes_filtered = remove_genes.remove_genes_in_file(gene_base_data, remove_genes_data)

    genes_filtered.to_csv(result_filename, index=False)


def generate_genes_from_uniprot_ensembl_db(uniprot_db_filename: str,
                                           ensembl_db_filename: str,
                                           proteins_filename: str,
                                           result_filename: str = 'gene_uniprot_ensembl_merged.csv',
                                           ) -> None:

    uniprots = utils.read_data_table_from_file(uniprot_db_filename)
    ensembls = utils.read_data_table_from_file(ensembl_db_filename)
    proteins = utils.read_data_table_from_file(proteins_filename)

    result = mergers_genes.merge_genes_from_uniprot_ensembl_db(ensembls, proteins, uniprots)

    result.to_csv(result_filename, index=False)


def add_hla_genes(gene_base_filename: str,
                  hla_genes_filename: str,
                  result_filename: str = 'gene_hla.csv',
                  ) -> None:

    gene_base = utils.read_data_table_from_file(gene_base_filename)
    hla_genes = utils.read_data_table_from_file(hla_genes_filename)

    genes_merged = gene_base.append(hla_genes, ignore_index=True)

    genes_merged.to_csv(result_filename, index=False)


def validate_gene_list(gene_filename: str) -> None:
    genes = utils.read_data_table_from_file(gene_filename)

    if gene_validators.validate_genes(genes):
        print('GENE LIST IS VALID')

    else:
        print('GENE LIST IS NOT VALID')
