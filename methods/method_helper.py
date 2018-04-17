import pandas as pd


def find_noncommon_gene_interactions(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
    index_1 = dataframe1.index.values
    index_2 = dataframe2.index.values

    unique_in_index_1 = []

    for index in index_1:
        if index not in index_2:
            unique_in_index_1.append(index)

    unique_in_index_2 = []

    for index in index_2:
        if index not in index_1:
            unique_in_index_2.append(index)

    print('Unique in index 1:')
    print(unique_in_index_1)

    print('Unique in index 2:')
    print(unique_in_index_2)

    print('Duplicated interactions index 1')
    series_1 = pd.Series(index_1)
    duplicated_1 = series_1[series_1.duplicated()]
    print(duplicated_1)
    print(len(duplicated_1))

    print('Duplicated interactions index 2')
    series_2 = pd.Series(index_2)
    duplicated_2 = series_2[series_2.duplicated()]
    print(duplicated_2)

    print('Non duplicated: ')
    print('series1: {}'.format(len(series_1.drop_duplicates())))
    print('series1: {}'.format(len(series_2.drop_duplicates())))


if __name__ == '__main__':
    original_means = pd.read_table('../method_tests/data/all_one_one_means.txt', index_col=0)
    result_means = pd.read_table('../methods/out/test_r_m_means_data-original_it-1000_in-100000.txt', index_col=0)

    find_noncommon_gene_interactions(original_means, result_means)
