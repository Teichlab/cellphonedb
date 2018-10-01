import pandas as pd


def validate_genes(genes: pd.DataFrame) -> bool:
    are_valid = True

    duplicated_genes = genes[genes.duplicated(keep=False)]

    if not duplicated_genes.empty:
        print('SOME GENES ARE DUPLICATED:')
        print(duplicated_genes.sort_values('ensembl').to_csv(index=False))
        are_valid = False

    return are_valid
