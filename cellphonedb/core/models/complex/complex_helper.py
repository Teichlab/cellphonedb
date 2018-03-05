import pandas as pd


def get_involved_complex_from_protein(proteins: pd.DataFrame, complexes: pd.DataFrame,
                                      complex_compositions: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
    """
    Returns a table of complex with all proteins declared in proteins.
    """

    complex_counts_composition = pd.merge(complex_compositions, proteins, left_on='protein_multidata_id',
                                          right_on='id_multidata')

    if complex_counts_composition.empty:
        return pd.DataFrame()

    def all_protein_involved(complex):
        number_proteins_in_counts = len(
            complex_counts_composition[
                complex_counts_composition['complex_multidata_id'] == complex['complex_multidata_id']])

        if number_proteins_in_counts < complex['total_protein']:
            return False

        return True

    complex_counts_composition = complex_counts_composition[
        complex_counts_composition.apply(all_protein_involved, axis=1)]

    complex_counts_composition = pd.merge(complex_counts_composition, complexes,
                                          left_on='complex_multidata_id',
                                          right_on='id_multidata',
                                          suffixes=['_protein', ''])

    if drop_duplicates:
        complex_counts_composition.drop_duplicates(['complex_multidata_id'], inplace=True)
    return complex_counts_composition
