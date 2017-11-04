import os

import pandas as pd
import zipfile

from tools.app import current_dir, data_dir, output_dir
from cellcommdb.tools.filters import remove_not_defined_columns

import requests


def _unzip_inwebinbiomap(file_path):
    zip_ref = zipfile.ZipFile(file_path, 'r')
    extract_path = '%s/temp' % (current_dir)
    zip_ref.extractall(extract_path)
    zip_ref.close()


def _download_inwebinbiomap():
    print('Downloading InBio_Map_core_2016_09_12')
    s = requests.Session()
    # First, we need create session in inatomics
    namefile = 'InBio_Map_core_2016_09_12.zip'
    r = s.get("https://www.intomics.com/inbio/api/login_guest?ref=&_=1509120239303")
    r = s.get('https://www.intomics.com/inbio/map/api/get_data?file=%s' % namefile)
    print('Downloaded InBio_Map_core_2016_09_12')

    download_path = '%s/temp/InBio_Map_core_2016_09_12.zip' % (current_dir)
    file = open(download_path, 'wb')
    file.write(r.content)
    file.close()

    _unzip_inwebinbiomap(download_path)

    return '%s/temp/InBio_Map_core_2016_09_12/core.psimitab' % current_dir


def only_noncomplex_interactions(complexes_namefile, inweb_namefile):
    if os.path.isfile('%s/%s' % (data_dir, inweb_namefile)):
        inweb_file = os.path.join(data_dir, inweb_namefile)
    else:
        inweb_file = os.path.join(output_dir, inweb_namefile)

    complexes_file = os.path.join(current_dir, 'data', complexes_namefile)

    complexes_df = pd.read_csv(complexes_file)

    proteins_in_complex = []

    for i in range(1, 5):
        proteins_in_complex = proteins_in_complex + complexes_df['protein_%s' % i].dropna().tolist()

    proteins_in_complex = list(set(proteins_in_complex))

    inweb_df = pd.read_csv(inweb_file)

    inweb_df_no_complex = inweb_df[inweb_df['protein_1'].apply(
        lambda protein: protein not in proteins_in_complex
    )]
    inweb_df_no_complex = inweb_df_no_complex[
        inweb_df_no_complex['protein_2'].apply(
            lambda protein: protein not in proteins_in_complex
        )]

    output_name = 'inweb_interactions_no_complex.csv'
    inweb_df_no_complex.to_csv('%s/out/%s' % (current_dir, output_name), index=False, float_format='%.4f')


def generate_inweb_interactions(inweb_inbiomap_namefile, database_proteins_namefile):
    if not inweb_inbiomap_namefile:
        inweb_inbiomap_namefile = _download_inwebinbiomap()
        inweb_inbiomap_file = os.path.join(inweb_inbiomap_namefile)
    else:
        inweb_inbiomap_file = os.path.join(current_dir, 'data', inweb_inbiomap_namefile)

    inweb_inbiomap_df = pd.read_csv(inweb_inbiomap_file, delimiter='\t', na_values='-')

    inweb_interactions = pd.DataFrame()

    inweb_interactions['protein_1'] = inweb_inbiomap_df.take([0], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['protein_2'] = inweb_inbiomap_df.take([1], axis=1).apply(
        lambda protein: protein.values[0].split(':')[1], axis=1)
    inweb_interactions['score_1'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: 0 if protein.values[0].split('|')[0] == '-' else protein.values[0].split('|')[0], axis=1)
    inweb_interactions['score_2'] = inweb_inbiomap_df.take([14], axis=1).apply(
        lambda protein: 0 if protein.values[0].split('|')[1] == '-' else protein.values[0].split('|')[1], axis=1)

    database_proteins_file = os.path.join(current_dir, 'data', database_proteins_namefile)

    database_proteins_df = pd.read_csv(database_proteins_file)

    inweb_interactions = _only_uniprots_in_df(database_proteins_df, inweb_interactions)

    output_name = 'cellphone_inweb.csv'

    inweb_interactions.to_csv('%s/%s' % (output_dir, output_name), index=False)


def remove_interactions_in_file(interaction_namefile, interactions_to_remove_namefile):
    if os.path.isfile('%s/%s' % (data_dir, interaction_namefile)):
        interactions_file = os.path.join(data_dir, interaction_namefile)
    else:
        interactions_file = os.path.join(output_dir, interaction_namefile)

    interactions_df = pd.read_csv(interactions_file)
    interactions_remove_df = pd.read_csv('%s/%s' % (data_dir, interactions_to_remove_namefile))

    def interaction_not_exists(row):
        if len(interactions_remove_df[(row['protein_1'] == interactions_remove_df['protein_1']) & (
                    row['protein_2'] == interactions_remove_df['protein_2'])]):
            return False

        if len(interactions_remove_df[(row['protein_1'] == interactions_remove_df['protein_2']) & (
                    row['protein_2'] == interactions_remove_df['protein_1'])]):
            return False

        return True

    interactions_filtered = interactions_df[interactions_df.apply(interaction_not_exists, axis=1)]

    interactions_filtered.to_csv('%s/interactions_cleaned.csv' % (output_dir), index=False)


def append_curated(interaction_namefile, interaction_curated_namefile):
    if os.path.isfile('%s/%s' % (data_dir, interaction_namefile)):
        interactions_file = os.path.join(data_dir, interaction_namefile)
    else:
        interactions_file = os.path.join(output_dir, interaction_namefile)

    interactions_df = pd.read_csv(interactions_file)
    interaction_curated_df = pd.read_csv('%s/%s' % (data_dir, interaction_curated_namefile))

    interactions_df['source'] = 'inweb'

    interactions_df.rename(index=str, columns={'protein_1': 'multidata_name_1', 'protein_2': 'multidata_name_2'},
                           inplace=True)

    interactions_merged = interactions_df.append(interaction_curated_df)

    interactions_merged.to_csv('%s/interaction.csv' % output_dir, index=False)


def _only_uniprots_in_df(uniprots_df, inweb_interactions):
    inweb_cellphone = pd.merge(inweb_interactions, uniprots_df, left_on=['protein_2'],
                               right_on=['uniprot'], how='inner')

    remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)

    inweb_cellphone = pd.merge(inweb_cellphone, uniprots_df, left_on=['protein_1'],
                               right_on=['uniprot'], how='inner')
    remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)

    # Prevents duplicated interactions if any uniprot is duplicated in uniprots_df
    inweb_cellphone = inweb_cellphone[inweb_cellphone.duplicated() == False]

    return remove_not_defined_columns(inweb_cellphone, inweb_interactions.columns.values)
