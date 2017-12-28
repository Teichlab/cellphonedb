import os
import pandas as pd

from cellphonedb.api import current_dir


def set_protein_type(protein_file):
    csv_proteins_df = pd.read_csv(protein_file)

    csv_proteins_df['membrane_type'] = None
    _defineProteinType(csv_proteins_df, 'Single-pass+type+I.csv', 'singlepass_typeI')
    _defineProteinType(csv_proteins_df, 'Single-pass+type+II.csv', 'singlepass_typeII')
    _defineProteinType(csv_proteins_df, 'Single-pass+type+III.csv', 'singlepass_typeIII')
    _defineProteinType(csv_proteins_df, 'Single-pass+type+IV.csv', 'singlepass_typeIV')
    _defineProteinType(csv_proteins_df, 'Multi-pass.csv', 'multipass')
    _defineProteinType(csv_proteins_df, 'GPI-anchor.csv', 'GPI-anchor')


def _defineProteinType(proteins_df, protein_type_file, type_name):
    protein_type_file = os.path.join(current_dir, 'data', protein_type_file)
    proteins_type_x = pd.read_csv(protein_type_file, sep=';')['Entry'].tolist()

    proteins_df['membrane_type'][proteins_df.apply(
        lambda x: x['uniprot'] in proteins_type_x, axis=1)] = type_name
