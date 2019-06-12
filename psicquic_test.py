#!/usr/bin/env python3
import sys
from io import StringIO

import pandas as pd
import requests
import tqdm as tqdm

proteins = pd.read_csv(sys.argv[1])['uniprot'].tolist()

sources = \
    {
        # 'InnateDB': 'https://psicquic.curated.innatedb.com/webservices/current/search/query/',
        # 'InnateDB-All': 'https://psicquic.all.innatedb.com/webservices/current/search/query/{}',
        'IMEx': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/imex/webservices/current/search/query/{}',
        'IntAct': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/intact/webservices/current/search/query/{}',
        'bhf-ucl': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/bhf-ucl/webservices/current/search/query/{}',
        'MatrixDB': 'http://matrixdb.univ-lyon1.fr:8080/psicquic/webservices/current/search/query/{}',
        'MINT': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/mint/webservices/current/search/query/{}',
        'I2D': 'http://ophid.utoronto.ca/psicquic-ws/webservices/current/search/query/{}',
        'UniProt': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/uniprot/webservices/current/search/query/{}',
        'MBInfo': 'http://www.ebi.ac.uk/Tools/webservices/psicquic/mbinfo/webservices/current/search/query/{}',
        # 'DIP': 'http://imex.mbi.ucla.edu/xpsq-dip-all/service/rest/current/search/query/{}',

    }

# # Create interaction_imex_raw.csv with all sources
#
# carry = pd.DataFrame()
#
# for source in sources.keys():
#     print('\n')
#     print(source)
#     for idx, chunk in tqdm.tqdm(enumerate(zip(*[iter(proteins)] * 300))):
#         url = sources[source].format('{}'.format(' or '.join(chunk)))
#         response = requests.get(url)
#
#         if response.text:
#             s = StringIO(response.text)
#             df = pd.read_csv(s, sep='\t', header=None)
#             carry = pd.concat([carry, df], sort=False, axis=0)
#         else:
#             print(url)
#             print('{} it {} is empty. Status code: {}'.format(source, idx, response.status_code))
#     carry['provider'] = source
#     carry.to_csv('out/psicquic/{}_interaction_raw.csv'.format(source), index=False)
#
carry = pd.DataFrame(columns=['A', 'B', 'altA', 'altB', 'provider'])

print('InnateDB')
innatedb = pd.read_csv('out/psicquic/InnateDB_interaction_raw.txt', sep='\t')[['A', 'B', 'altA', 'altB']]
innatedb['provider'] = 'InnateDB'
carry = carry.append(innatedb)

print('InnateDB-All')
innatedb_all = pd.read_csv('out/psicquic/InnateDB-All_interaction_raw.txt', sep='\t')[
    ['A', 'B', 'altA', 'altB']]
innatedb_all['provider'] = 'InnateDB-All'
carry = carry.append(innatedb_all)

for source in sources.keys():
    print(source)
    source_data = pd.read_csv('out/psicquic/{}_interaction_raw.csv'.format(source))
    source_data.rename(columns={'0': 'A', '1': 'B', '2': 'altA', '3': 'altB'}, index=str, inplace=True)
    carry = carry.append(source_data[['A', 'B', 'altA', 'altB', 'provider']], sort=False, ignore_index=True)

carry.to_csv('out/IMEX_all_sources.csv', index=False)
