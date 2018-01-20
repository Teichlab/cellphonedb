from unittest import TestCase

import pandas as pd

from cellphonedb.models.multidata import properties_multidata


class TestPropertiesMultidata(TestCase):
    def test_is_ligand(self):
        multidatas = pd.DataFrame(multidatas_fixtures)

        for index, multidata in multidatas.iterrows():
            self.assertEqual(properties_multidata.is_ligand(multidata), multidata['is_ligand'],
                             'Multidata %s is not ligand' % multidata['id'])

    def test_is_receptor(self):
        multidatas = pd.DataFrame(multidatas_fixtures)
        for index, multidata in multidatas.iterrows():
            self.assertEqual(properties_multidata.is_receptor(multidata), multidata['is_receptor'])


multidatas_fixtures = [
    {
        'id': 1,
        'receptor': True,
        'secretion': True,
        'other': False,
        'transmembrane': False,
        'extracellular': False,
        'cytoplasm': False,
        'transporter': False,
        'is_ligand': True,
        'is_receptor': False,
        'secreted_highlight': True

    },
    {
        'id': 2,
        'receptor': True,
        'secretion': False,
        'other': False,
        'transmembrane': True,
        'extracellular': True,
        'cytoplasm': False,
        'transporter': False,
        'is_ligand': True,
        'is_receptor': True,
        'secreted_highlight': False

    },
    {
        'id': 3,
        'receptor': True,
        'secretion': False,
        'other': False,
        'transmembrane': False,
        'extracellular': False,
        'cytoplasm': False,
        'transporter': False,
        'is_ligand': False,
        'is_receptor': False,
        'secreted_highlight': False
    },
    {
        'id': 4,
        'receptor': False,
        'secretion': False,
        'other': False,
        'transmembrane': False,
        'extracellular': False,
        'cytoplasm': False,
        'transporter': False,
        'is_ligand': False,
        'is_receptor': False,
        'secreted_highlight': False
    },
]
