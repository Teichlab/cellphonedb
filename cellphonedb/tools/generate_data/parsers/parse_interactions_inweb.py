import os
import zipfile

import pandas as pd
import requests

from tools.app import current_dir, output_dir
from tools.interactions_helper import _only_uniprots_in_df


def generate_interactions_inweb(inweb_inbiomap_namefile, database_proteins_namefile):
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

    inweb_interactions['source'] = 'inweb'

    database_proteins_file = os.path.join(current_dir, 'data', database_proteins_namefile)

    database_proteins_df = pd.read_csv(database_proteins_file)

    inweb_interactions = _only_uniprots_in_df(database_proteins_df, inweb_interactions)

    inweb_interactions.to_csv('%scellphone_interactions_inweb.csv' % output_dir, index=False)


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


def _unzip_inwebinbiomap(file_path):
    zip_ref = zipfile.ZipFile(file_path, 'r')
    extract_path = '%s/temp' % (current_dir)
    zip_ref.extractall(extract_path)
    zip_ref.close()
