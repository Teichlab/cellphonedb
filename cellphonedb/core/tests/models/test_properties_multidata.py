from unittest import TestCase

import pandas as pd

from cellphonedb.core.models.multidata import properties_multidata


class TestPropertiesMultidata(TestCase):
    def test_is_secreted_ligand(self):
        multidatas = pd.DataFrame(multidatas_fixtures)

        for index, multidata in multidatas.iterrows():
            self.assertEqual(properties_multidata.is_secreted_ligand(multidata), multidata['is_secreted_ligand'],
                             'Multidata {} secreted ligand dont match'.format(multidata['id']))
            self.assertEqual(properties_multidata.is_transmembrane_ligand(multidata),
                             multidata['is_transmembrane_ligand'],
                             'Multidata {} transmembrane ligand dont match'.format(multidata['id']))

    def test_is_receptor(self):
        multidatas = pd.DataFrame(multidatas_fixtures)
        for index, multidata in multidatas.iterrows():
            self.assertEqual(properties_multidata.is_receptor(multidata), multidata['is_receptor'],
                             'Multidata {} receptor dont match')


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
        'is_secreted_ligand': True,
        'is_transmembrane_ligand': False,
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
        'is_secreted_ligand': False,
        'is_transmembrane_ligand': True,
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
        'is_secreted_ligand': False,
        'is_transmembrane_ligand': False,
        'is_receptor': False,
        'secreted_highlight': False
    },
    {
        'id': 4,
        'receptor': False,
        'secretion': False,
        'other': False,
        'transmembrane': True,
        'extracellular': False,
        'cytoplasm': False,
        'transporter': False,
        'is_secreted_ligand': False,
        'is_transmembrane_ligand': True,
        'is_receptor': False,
        'secreted_highlight': False
    },
]
