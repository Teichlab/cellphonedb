import hashlib
import http
import urllib.request
from datetime import datetime
from http import server
from urllib.error import URLError

import pandas as pd


def call(local_filename: str,
         download_base_path: str,
         default_download_response: str = None,
         ) -> pd.DataFrame:

    url = 'http://www.guidetopharmacology.org/DATA/interactions.csv'

    try:
        response = urllib.request.urlopen(url)
        iuphar_interaction = response.read().decode('utf-8')

        web_checksum = hashlib.sha1(iuphar_interaction.encode('utf-8')).hexdigest()

        is_same_file = validate_checksum(web_checksum, local_filename)

        if not is_same_file:
            print('WARNING: THE GUIDETOPHARMACOLOGY DATA IS DIFFERENT TO {} LOCAL FILE'.format(local_filename))
            answers = {'yes': True, '': True, 'no': False}

            while True:
                print('DO YOU WANT TO DOWNLOAD AND USE IT? YES/no ')
                if default_download_response in answers:
                    response = default_download_response
                    print(response)
                    break

                response = input().lower()
                if response in answers:
                    break

            if answers[response]:
                new_name = 'interaction_iuphar_guidetopharmacology__{}.csv'.format(datetime.now().strftime("%Y%m%d"))

                downloaded_file = '{}/{}'.format(download_base_path, new_name)

                with open(downloaded_file, 'w', encoding='utf-8') as iuphar_file:
                    iuphar_file.write(iuphar_interaction)

                print('FILE UPDATED AND SAVED IN {}'.format(downloaded_file))

                local_filename = downloaded_file

        else:
            print('IUPHAR INPUT DATA IS UP TO DATE')

    except URLError as e:

        if hasattr(e, 'code') and e.code in server.BaseHTTPRequestHandler.responses:
            print(http.server.BaseHTTPRequestHandler.responses[e.code])

        else:
            print(e)

        print('ERROR: CANT GET GUIDETOPHARMACOLOGY INTERACTION DATA FROM ORIGINAL SOURCE. USING LOCAL SOURCE')

    print('LOADING IUPHAR DATA FROM {}'.format(local_filename))
    return pd.read_csv(local_filename, dtype='str')


def validate_checksum(original_checksum: str, filename: str) -> bool:
    sha1sum = hashlib.sha1()
    chunk_size = 2 ** 16
    with open(filename, 'rb') as source:
        block = source.read(chunk_size)
        while block:
            sha1sum.update(block)
            block = source.read(chunk_size)
    read_checksum = sha1sum.hexdigest()

    return read_checksum == original_checksum
