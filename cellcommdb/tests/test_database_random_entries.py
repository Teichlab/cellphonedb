import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.config import TestConfig
from cellcommdb.extensions import db
from cellcommdb.models import Complex, Multidata

complex_entries = [
    {
        'multidata': {
            "name": "5HT3C5HT3A complex",
            "receptor": True,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": True,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Note: Presumably retained within the endoplasmic reticulum unless complexed with HTR3A."
        },
        'composition': {
            "protein_1": "Q8WXA8",
            "protein_2": "P46098",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "a2Bb3 complex",
            "receptor": False,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": True,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "True",
            "pdb_id": "1kup",
            "stoichiometry": "ITGA2B;ITGB3",
            "comments": "Well known integrin combination"
        },
        'composition': {
            "protein_1": "P08514",
            "protein_2": "P05106",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "Agrin complex",
            "receptor": True,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "partial",
            "pdb_id": "3ml4",
            "stoichiometry": "DOK7;DOK7;MUSK;MUSK",
            "comments": "MUSK Interacts with LRP4; the heterodimer forms an AGRIN receptor complex that binds AGRIN resulting in activation of MUSK "
        },
        'composition': {
            "protein_1": "O15146",
            "protein_2": "O00468",
            "protein_3": "O75096",
            "protein_4": "Q18PE1"

        }
    },
    {
        'multidata': {
            "name": "CD79_IGHM receptor",
            "receptor": True,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Membrane-bound IgM molecules are non-covalently associated with heterodimer of CD79A and CD79B"
        },
        'composition': {
            "protein_1": "P11912",
            "protein_2": "P40259",
            "protein_3": "P01871",
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "BMPR1B complex",
            "receptor": True,
            "receptor_highlight": True,
            "receptor_desc": "TGFBeta_receptor_add",
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Serine/threonine kinase heterodimer upon ligand binding"
        },
        'composition': {
            "protein_1": "O00238",
            "protein_2": "Q13873",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "CD1A complex",
            "receptor": False,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": True,
            "other_desc": "T cell",
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "True",
            "pdb_id": "1onq",
            "stoichiometry": "B2M;CD1A",
            "comments": "Heterodimer with B2M (beta-2-microglobulin)."
        },
        'composition': {
            "protein_1": "P61769",
            "protein_2": "P06126",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "IL17 AF",
            "receptor": False,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": True,
            "secreted_desc": "Cytokine",
            "transmembrane": False,
            "secretion": True,
            "peripheral": False,
            "ligand": True,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": None
        },
        'composition': {
            "protein_1": "Q16552",
            "protein_2": "Q96PD4",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "IL17 AF",
            "receptor": False,
            "receptor_highlight": False,
            "receptor_desc": None,
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": True,
            "secreted_desc": "Cytokine",
            "transmembrane": False,
            "secretion": True,
            "peripheral": False,
            "ligand": True,
            "adaptor": False
        },
        'complex': {
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": None
        },
        'composition': {
            "protein_1": "Q16552",
            "protein_2": "Q96PD4",
            "protein_3": None,
            "protein_4": None

        }
    },
    {
        'multidata': {
            "name": "IL17 receptor AC",
            "receptor": True,
            "receptor_highlight": True,
            "receptor_desc": "Cytokine receptor IL17 family",
            "adhesion": False,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secretion": False,
            "peripheral": False,
            "ligand": False,
            "adaptor": False
        },
        'complex':
            {
                "pdb_structure": "FALSE",
                "pdb_id": None,
                "stoichiometry": None,
                "comments": "NA; the heterodimer binds IL17AF",
            },
        'composition':
            {
                "protein_1": "Q96F46",
                "protein_2": "Q8NAC3",
                "protein_3": None,
                "protein_4": None,
            }

    }
]


class DatabaseRandomEntries(TestCase):
    def test_complex(self):
        query = db.session.query(Multidata)
        dataframe = pd.read_sql(query.statement, db.engine)

        data_not_match = False

        for complex in complex_entries:
            db_complex = dataframe[dataframe['name'] == complex['multidata']['name']]

            for multidata_column in complex['multidata']:

                if db_complex[multidata_column].iloc[0] != complex['multidata'][multidata_column]:
                    print('Failed checking column \'%s\' of multidata with name \'%s\'' % (
                    multidata_column, complex['multidata']['name']))
                    print('Expected value: %s' % complex['multidata'][multidata_column])
                    print('Database value: %s' % db_complex[multidata_column].iloc[0])
                    print('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some multidata doesnt match')

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        self.client = self.app.test_client()
