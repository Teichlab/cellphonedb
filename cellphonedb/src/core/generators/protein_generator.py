import pandas as pd

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.core.generators import generator_helper


def protein_generator(uniprot_db: pd.DataFrame,
                      curated_proteins: pd.DataFrame,
                      user_protein: pd.DataFrame,
                      default_values: dict,
                      default_types: dict,
                      log_path: str) -> pd.DataFrame:
    result = _merge_proteins(curated_proteins, uniprot_db, default_values, default_types, log_path)

    if user_protein:
        result = _merge_proteins(user_protein, result, default_values, default_types, log_path)

    return result


def _merge_proteins(base: pd.DataFrame,
                    additional: pd.DataFrame,
                    default_values: dict,
                    default_types: dict,
                    log_file: str) -> pd.DataFrame:
    additional = additional.copy()

    used_cols = ['uniprot', 'protein_name'] + list(default_values.keys())

    # homogeneized column names
    additional.rename(index=str, columns={'Entry': 'uniprot', 'Entry name': 'protein_name'}, inplace=True)

    # Here we set defaults for uniprot & curated data
    base = generator_helper.set_defaults(base, default_values)
    additional = generator_helper.set_defaults(additional, default_values)

    # we will only use these columns
    additional: pd.DataFrame = additional[used_cols]
    base: pd.DataFrame = base[used_cols]

    # Type casting to ensure they are equal
    additional = additional.astype(default_types)
    base = base.astype(default_types)

    additional_is_in_curated = additional['uniprot'].isin(base['uniprot'])
    curated_is_in_additional = base['uniprot'].isin(additional['uniprot'])

    common_additional: pd.DataFrame = additional.reindex(used_cols, axis=1)[additional_is_in_curated]
    common_curated: pd.DataFrame = base.reindex(used_cols, axis=1)[curated_is_in_additional]

    distinct_additional = additional[~additional_is_in_curated]
    distinct_curated = base[~curated_is_in_additional]

    result: pd.DataFrame = pd.concat([common_curated, distinct_additional, distinct_curated],
                                     ignore_index=True).sort_values(by='uniprot')

    if not common_curated.equals(common_additional):
        app_logger.warning('There are differences between merged files: logged to {}'.format(log_file))

        common_curated['file'] = 'curated'
        common_additional['file'] = 'additional'

        log = common_curated.append(common_additional).sort_values(by=used_cols)
        log.to_csv(log_file, index=False, sep='\t')

    return result
