import os

import pandas as pd

from tools.app import current_dir


def merge_duplicated_proteins(protein_file):
    bools = ['transmembrane', 'secretion', 'peripheral', 'receptor', 'adhesion', 'other', 'transporter',
             'secreted_highlight', 'cytoplasm', 'extracellular']

    csv_proteins_df = pd.read_csv('%s/data/%s' % (current_dir, protein_file))

    csv_proteins_df[bools] = csv_proteins_df[bools].astype(bool)

    csv_proteins_df.rename(index=str, columns={'name': 'uniprot'}, inplace=True)

    unique_prots = _merge_same_proteins(csv_proteins_df, bools)

    output_name = _filename_parameter(protein_file, 'merged')

    unique_prots.to_csv('%s/out/%s' % (current_dir, output_name), index=False)


def _filename_parameter(protein_file, parameter):
    splited_filename = protein_file.split('.')
    splited_filename[-2] = '%s_%s' % (splited_filename[-2], parameter)
    output_name = '.'.join(splited_filename)
    return output_name


def _merge_same_proteins(all_prot_df, bools):
    unique_prots = all_prot_df.drop_duplicates(subset=['uniprot'])

    def merge_values(row):
        protein = all_prot_df[all_prot_df['uniprot'] == row['uniprot']]

        def setNonEmptyStrings(protRow):
            row[protRow.notnull()] = protRow[protRow.notnull()]

        protein.apply(
            setNonEmptyStrings, axis=1
        )

        row[bools] = protein[bools].any()

        return row

    unique_prots = unique_prots.apply(

        merge_values, axis=1
    )

    return unique_prots
