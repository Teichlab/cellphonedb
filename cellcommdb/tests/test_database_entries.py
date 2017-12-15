import pandas as pd
from flask_testing import TestCase

from cellcommdb.api import create_app
from cellcommdb.config import TestConfig
from cellcommdb.extensions import db
from cellcommdb.models.complex.db_model_complex import Complex
from cellcommdb.models.complex_composition.db_model_complex_composition import ComplexComposition
from cellcommdb.models.gene.db_model_gene import Gene
from cellcommdb.models.interaction.db_model_interaction import Interaction
from cellcommdb.models.multidata.db_model_multidata import Multidata
from cellcommdb.models.protein.db_model_protein import Protein
from cellcommdb.unblend import Unblend

complex_entries = [
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "FALSE",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Note: Presumably retained within the endoplasmic reticulum unless complexed with HTR3A.",
            "extracellular": False,
        },
        'composition': ["Q8WXA8", "P46098"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "TRUE",
            "pdb_id": "1kup",
            "stoichiometry": "ITGA2B;ITGB3",
            "comments": "Well known integrin combination"
        },
        'composition':
            ["P08514", "P05106"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "partial",
            "pdb_id": "3ml4",
            "stoichiometry": "DOK7;DOK7;MUSK;MUSK",
            "comments": "MUSK Interacts with LRP4; the heterodimer forms an AGRIN receptor complex that binds AGRIN resulting in activation of MUSK",
            "extracellular": False,
        },
        'composition':
            ["O15146", "O00468", "O75096", "Q18PE1"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "FALSE",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Membrane-bound IgM molecules are non-covalently associated with heterodimer of CD79A and CD79B",
            "extracellular": False,
        },
        'composition':
            ["P11912", "P40259", "P01871"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "FALSE",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "Serine/threonine kinase heterodimer upon ligand binding",
            "extracellular": False,
        },
        'composition':
            ["O00238", "Q13873"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "TRUE",
            "pdb_id": "1onq",
            "stoichiometry": "B2M;CD1A",
            "comments": "Heterodimer with B2M (beta-2-microglobulin).",
            "extracellular": False,
        },
        'composition':
            ["P61769", "P06126"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "FALSE",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": None,
            "extracellular": True,
        },
        'composition':
            ["Q16552", "Q96PD4"]
    },
    {
        'data': {
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
            "cytoplasm": False,
            "pdb_structure": "FALSE",
            "pdb_id": None,
            "stoichiometry": None,
            "comments": "NA; the heterodimer binds IL17AF",
            "extracellular": False,
        },
        'composition':
            ["Q96F46", "Q8NAC3"]
    }
]
protein_entries = [
    {
        "name": "A0A0B4J2F0",
        "entry_name": "PIOS1_HUMAN",
        "transmembrane": False,
        "secretion": True,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    },
    {
        "name": "A0AVI2",
        "entry_name": "FR1L5_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "A1E959",
        "entry_name": "ODAM_HUMAN",
        "transmembrane": False,
        "secretion": True,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": True,
        "extracellular": True,
    },
    {
        "name": "O75970",
        "entry_name": "MPDZ_HUMAN",
        "transmembrane": False,
        "secretion": False,
        "peripheral": True,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": True,
        "extracellular": False,
    },
    {
        "name": "O76036",
        "entry_name": "NCTR1_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "O95256",
        "entry_name": "I18RA_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": True,
        "receptor_desc": "Cytokine_receptor_add",
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": "Iglike",
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "P78357",
        "entry_name": "CNTP1_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": True,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": "complex",
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "Q13444",
        "entry_name": "ADA15_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": True,
        "other": True,
        "other_desc": "disintegrin and metalloproteinase",
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": "Active metalloproteinase with gelatinolytic and collagenolytic activity. (uniprot)",
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "A5X5Y0",
        "entry_name": "5HT3E_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": True,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "Q9NPH3",
        "entry_name": "IL1AP_HUMAN",
        "transmembrane": True,
        "secretion": True,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": True,
        "receptor_desc": "Cytokine_receptor_add",
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": True,
        "secreted_desc": "Cytokine",
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    },
    {
        "name": "O75325",
        "entry_name": "LRRN2_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add | To_comment",
        "tags_reason": "Iglike | Possible_receptor",
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    },
    {
        "name": "P05067",
        "entry_name": "A4_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": False,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": True,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": "ligandIUPHAR",
        "ligand": True,
        "cytoplasm": True,
        "extracellular": True,
    },
    {
        "name": "Q9HC73",
        "entry_name": "CRLF2_HUMAN",
        "transmembrane": True,
        "secretion": True,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    },
    {
        "name": "P48960",
        "entry_name": "CD97_HUMAN",
        "transmembrane": True,
        "secretion": True,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": False,
        "receptor_desc": None,
        "adhesion": True,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": False,
    },
    {
        "name": "Q01113",
        "entry_name": "IL9R_HUMAN",
        "transmembrane": True,
        "secretion": True,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": True,
        "receptor_desc": "Cytokine_receptor_add",
        "adhesion": False,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": True,
        "secreted_desc": "Cytokine",
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    },
    {
        "name": "P16284",
        "entry_name": "PECA1_HUMAN",
        "transmembrane": True,
        "secretion": False,
        "peripheral": False,
        "receptor": True,
        "receptor_highlight": True,
        "receptor_desc": "Inflammation",
        "adhesion": True,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "ligand": False,
        "cytoplasm": False,
        "extracellular": True,
    }
]
gene_entries = [
    {
        "ensembl": "ENSG00000127837",
        "gene_name": "AAMP",
        "name": "Q13685"
    },
    {
        "ensembl": "ENSG00000102468",
        "gene_name": "HTR2A",
        "name": "P28223"
    }
]
interaction_entries = [
    {
        "score_1": 1,
        "score_2": 1,
        "multidata_name_1": "CD8 receptor",
        "multidata_name_2": "P06239",
        "comments": "1q69, PDB partially",
        "source": "curated"
    },
    {
        "score_1": 0.35,
        "score_2": 0.35,
        "multidata_name_1": "P25106",
        "multidata_name_2": "P25705",
        "comments": None,
        "source": "IntAct"
    },
    {
        "score_1": 0.35,
        "score_2": 0.35,
        "multidata_name_1": "P01023",
        "multidata_name_2": "P25705",
        "comments": None,
        "source": "MINT"
    },
    {
        "score_1": 0.92,
        "score_2": 0.92,
        "multidata_name_1": "Q05397",
        "multidata_name_2": "P12931",
        "comments": None,
        "source": "MolCon"
    },
    {
        "score_1": 0.44,
        "score_2": 0.44,
        "multidata_name_1": "Q03167",
        "multidata_name_2": "P01137",
        "comments": None,
        "source": "I2D-IMEx"
    },
    {
        "score_1": 0.0,
        "score_2": 1.0,
        "multidata_name_1": "O00421",
        "multidata_name_2": "Q99731",
        "comments": None,
        "source": "InnateDB"
    },

]


class DatabaseRandomEntries(TestCase):
    def test_interaction(self):

        interaction_query = db.session.query(Interaction)
        interaction_df = pd.read_sql(interaction_query.statement, db.engine)

        interaction_df = Unblend.multidata(interaction_df, ['multidata_1_id', 'multidata_2_id'], 'multidata_name',
                                           True)

        data_not_match = False

        for interaction in interaction_entries:
            db_interaction = interaction_df

            for column_name in interaction:
                if interaction[column_name] == None:
                    db_interaction = db_interaction[pd.isnull(db_interaction[column_name])]
                else:
                    db_interaction = db_interaction[db_interaction[column_name] == interaction[column_name]]

            if (len(db_interaction) < 1):
                print('Failed cheking Interaction:')
                print('Expected data:')
                print(interaction)
                data_not_match = True

        self.assertFalse(data_not_match, 'Some Interactions doesnt match')

    def test_gene(self):
        query = db.session.query(Gene, Multidata).join(Protein).join(Multidata)
        dataframe = pd.read_sql(query.statement, db.engine)

        data_not_match = False

        for gene in gene_entries:
            db_gene = dataframe

            for column_name in gene:
                if gene[column_name] == None:
                    db_gene = db_gene[pd.isnull(db_gene[column_name])]
                else:
                    db_gene = db_gene[db_gene[column_name] == gene[column_name]]

            if (len(db_gene) < 1):
                print('Failed cheking Gene:')
                print('Expected data:')
                print(gene)
                data_not_match = True

        self.assertFalse(data_not_match, 'Some Gene doesnt match')

    def test_protein(self):
        query = db.session.query(Multidata, Protein).join(Protein)
        dataframe = pd.read_sql(query.statement, db.engine)

        data_not_match = False

        for protein in protein_entries:
            db_protein = dataframe[dataframe['name'] == protein['name']]

            for column_name in protein:
                if db_protein[column_name].iloc[0] != protein[column_name]:
                    print('Failed checking column \'%s\' of multidata/protein with name \'%s\'' % (
                        column_name, protein['name']))
                    print('Expected value: %s' % protein[column_name])
                    print('Database value: %s' % db_protein[column_name].iloc[0])
                    print('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some proteins doesnt match')

    def test_complex_composition_table(self):
        query_multidata = db.session.query(Multidata)
        df_multidata = pd.read_sql(query_multidata.statement, db.engine)

        query_complex_composition = db.session.query(ComplexComposition)
        df_complex_composition = pd.read_sql(query_complex_composition.statement, db.engine)

        number_compositions_not_match = False
        some_protein_didnt_exists = False
        some_protein_not_part_of_complex = False

        for complex in complex_entries:
            db_complex_id = df_multidata[df_multidata['name'] == complex['data']['name']]['id_multidata'].iloc[0]

            if len(df_complex_composition[df_complex_composition['complex_multidata_id'] != db_complex_id]) == len(
                    complex['composition']):
                print('Failed checking number of complex_composition with name \'%s\'' % (
                    complex['data']['name']))
                print('Expected value: %s' % len(
                    df_complex_composition[df_complex_composition['complex_multidata_id'] == db_complex_id]))
                print('Database value: %s' % len(complex['composition']))
                print('---')
                number_compositions_not_match = True

            for protein_name in complex['composition']:
                db_complex_composition_ids = \
                    df_complex_composition[df_complex_composition['complex_multidata_id'] == db_complex_id][
                        'protein_multidata_id'].tolist()

                composition_multidata_id = df_multidata[df_multidata['name'] == protein_name]['id_multidata']

                if not len(composition_multidata_id):
                    print('Failed finding protein \'%s\' in multidata from complex name \'%s\'' % (
                        protein_name, complex['data']['name']))
                    some_protein_didnt_exists = True
                    continue

                if composition_multidata_id.iloc[0] not in db_complex_composition_ids:
                    print('Failed finding protein \'%s\' in composition from complex name \'%s\'' % (
                        protein_name, complex['data']['name']))
                    some_protein_not_part_of_complex = True

        self.assertFalse(number_compositions_not_match, 'Number of complex composition doesnt match')
        self.assertFalse(some_protein_didnt_exists, 'Some complex_composition proteins doesnt match')
        self.assertFalse(some_protein_not_part_of_complex, 'Complex_composition proteins doesnt match')

    def test_complex(self):
        query = db.session.query(Multidata, Complex).join(Complex)
        dataframe = pd.read_sql(query.statement, db.engine)

        data_not_match = False

        for complex in complex_entries:
            db_complex = dataframe[dataframe['name'] == complex['data']['name']]

            for complex_data in complex['data']:
                if db_complex[complex_data].iloc[0] != complex['data'][complex_data]:
                    print('Failed checking column \'%s\' of multidata/complex with name \'%s\'' % (
                        complex_data, complex['data']['name']))
                    print('Expected value: %s' % complex['data'][complex_data])
                    print('Database value: %s' % db_complex[complex_data].iloc[0])
                    print('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some complex doesnt match')

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        self.client = self.app.test_client()
