import pandas as pd
from flask_testing import TestCase

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.flask.flask_app import create_app

complex_entries = [
    {
        'data': {
            "name": "5HT3C5HT3A complex",
            "receptor": True,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "transporter": True,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments_complex": "Note: Presumably retained within the endoplasmic reticulum unless complexed with HTR3A.",
            "integrin": False
        },
        'composition': ["Q8WXA8", "P46098"]
    },
    {
        'data': {
            "name": "a2Bb3 complex",
            "receptor": False,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "True",
            "pdb_id": "1kup",
            "stoichiometry": "ITGA2B;ITGB3",
            "comments_complex": "Well known integrin combination",
            "integrin": True

        },
        'composition':
            ["P08514", "P05106"]
    },
    {
        'data': {
            "name": "Agrin complex",
            "receptor": True,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "partial",
            "pdb_id": "3ml4",
            "stoichiometry": "DOK7;DOK7;MUSK;MUSK",
            "comments_complex": "MUSK Interacts with LRP4; the heterodimer forms an AGRIN receptor complex that binds AGRIN resulting in activation of MUSK",
            "integrin": False,
        },
        'composition':
            ["O15146", "O00468", "O75096", "Q18PE1"]
    },
    {
        'data': {
            "name": "CD79_IGHM receptor",
            "receptor": True,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments_complex": "Membrane-bound IgM molecules are non-covalently associated with heterodimer of CD79A and CD79B",
            "integrin": False,
        },
        'composition':
            ["P11912", "P40259", "P01871"]
    },
    {
        'data': {
            "name": "BMPR1B_BMPR2",
            "receptor": True,
            "receptor_desc": "TGFBeta_receptor_add",
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments_complex": "Serine/threonine kinase heterodimer upon ligand binding",
            "integrin": False,
        },
        'composition':
            ["O00238", "Q13873"]
    },
    {
        'data': {
            "name": "CD1A complex",
            "receptor": False,
            "receptor_desc": None,
            "other": True,
            "other_desc": "T cell",
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "True",
            "pdb_id": "1onq",
            "stoichiometry": "B2M;CD1A",
            "comments_complex": "Heterodimer with B2M (beta-2-microglobulin).",
            "integrin": False,
        },
        'composition':
            ["P61769", "P06126"]
    },
    {
        'data': {
            "name": "IL17 AF",
            "receptor": False,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": True,
            "secreted_desc": "Cytokine",
            "transmembrane": False,
            "secreted": True,
            "peripheral": False,
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments_complex": None,
            "integrin": False,
        },
        'composition':
            ["Q16552", "Q96PD4"]
    },
    {
        'data': {
            "name": "IL17 receptor AC",
            "receptor": True,
            "receptor_desc": "Cytokine receptor IL17 family",
            "other": False,
            "other_desc": None,
            "transporter": False,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "False",
            "pdb_id": None,
            "stoichiometry": None,
            "comments_complex": "NA; the heterodimer binds IL17AF",
            "integrin": False,
        },
        'composition':
            ["Q96F46", "Q8NAC3"]
    }
]
protein_entries = [
    {
        "name": "A0A0B4J2F0",
        "protein_name": "PIOS1_HUMAN",
        "transmembrane": False,
        "secreted": True,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "A0AVI2",
        "protein_name": "FR1L5_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "A1E959",
        "protein_name": "ODAM_HUMAN",
        "transmembrane": False,
        "secreted": True,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "O75970",
        "protein_name": "MPDZ_HUMAN",
        "transmembrane": False,
        "secreted": False,
        "peripheral": True,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "O76036",
        "protein_name": "NCTR1_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "O95256",
        "protein_name": "I18RA_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": "Cytokine_receptor_add",
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "Iglike",
    },
    {
        "name": "P78357",
        "protein_name": "CNTP1_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "complex",
    },
    {
        "name": "Q13444",
        "protein_name": "ADA15_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "Active metalloproteinase with gelatinolytic and collagenolytic activity. (uniprot)",
    },
    {
        "name": "A5X5Y0",
        "protein_name": "5HT3E_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": True,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "Q9NPH3",
        "protein_name": "IL1AP_HUMAN",
        "transmembrane": True,
        "secreted": True,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": "Cytokine_receptor_add",
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": True,
        "secreted_desc": "Cytokine",
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "O75325",
        "protein_name": "LRRN2_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add | To_comment",
        "tags_reason": None,
        "tags_description": "Iglike | Possible_receptor",
    },
    {
        "name": "P05067",
        "protein_name": "A4_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": False,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "ligandIUPHAR",
    },
    {
        "name": "Q9HC73",
        "protein_name": "CRLF2_HUMAN",
        "transmembrane": True,
        "secreted": True,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "P48960",
        "protein_name": "CD97_HUMAN",
        "transmembrane": True,
        "secreted": True,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": None,
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "Q01113",
        "protein_name": "IL9R_HUMAN",
        "transmembrane": True,
        "secreted": True,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": "Cytokine_receptor_add",
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": True,
        "secreted_desc": "Cytokine",
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
    },
    {
        "name": "P16284",
        "protein_name": "PECA1_HUMAN",
        "transmembrane": True,
        "secreted": False,
        "peripheral": False,
        "receptor": True,
        "receptor_desc": "Inflammation",
        "other": False,
        "other_desc": None,
        "transporter": False,
        "secreted_highlight": False,
        "secreted_desc": None,
        "tags": None,
        "tags_reason": None,
        "tags_description": None,
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
        "id_cp_interaction": "CPI-CS0A66DB1CA",
        "name_1": "CD8 receptor",
        "name_2": "P06239",
        "comments_interaction": "1q69, PDB partially",
        "source": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS0322F3EA0",
        "name_1": "Q03167",
        "name_2": "P01137",
        "comments_interaction": "uniprot",
        "source": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS0605AC9BF",
        "name_1": "Q99731",
        "name_2": "O00421",
        "comments_interaction": None,
        "source": "guidetopharmacology.org",
    },
    {
        "id_cp_interaction": "CPI-SS03165AD8C",
        "name_1": "O00590",
        "name_2": "P13500",
        "comments_interaction": "PMID: 24218476",
        "source": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS005572B52",
        "name_1": "P49767",
        "name_2": "P35916",
        "comments_interaction": "uniprot",
        "source": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS0AEED3EB0",
        "name_1": "Q9HC23",
        "name_2": "Q8NFJ6",
        "source": "guidetopharmacology.org",
        "comments_interaction": None
    },
    {
        "id_cp_interaction": "CPI-SS0B1B18F2D",
        "name_1": "P48061",
        "name_2": "P27487",
        "source": "curated",
        "comments_interaction": "PMID: 24218476"
    }
]


class TestValidatorDatabaseRandomEntries(TestCase):
    def test_interaction(self):

        interaction_df = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'interaction').get_all_expanded()

        data_not_match = False

        for interaction in interaction_entries:
            db_interaction = interaction_df
            non_match_properties = []
            for column_name in interaction:
                if interaction[column_name] == None:
                    db_interaction = db_interaction[pd.isnull(db_interaction[column_name])]
                else:
                    db_interaction = db_interaction[db_interaction[column_name] == interaction[column_name]]

                if len(db_interaction) < 1:
                    non_match_properties.append(column_name)
            if (len(db_interaction) < 1):
                app_logger.warning('Failed cheking Interaction:')
                app_logger.warning('Expected data:')
                app_logger.warning(interaction)
                app_logger.warning('Non Match properties')
                app_logger.warning(non_match_properties)
                data_not_match = True

        self.assertFalse(data_not_match, 'Some Interactions doesnt match')

    def test_gene(self):

        dataframe = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'gene').get_all_expanded()

        data_not_match = False

        for gene in gene_entries:
            db_gene = dataframe

            for column_name in gene:
                if gene[column_name] == None:
                    db_gene = db_gene[pd.isnull(db_gene[column_name])]
                else:
                    db_gene = db_gene[db_gene[column_name] == gene[column_name]]

            if (len(db_gene) < 1):
                app_logger.warning('Failed cheking Gene:')
                app_logger.warning('Expected data:')
                app_logger.warning(gene)
                data_not_match = True

        self.assertFalse(data_not_match, 'Some Gene doesnt match')

    def test_protein(self):

        dataframe = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'protein').get_all_expanded()

        data_not_match = False

        for protein in protein_entries:
            db_protein = dataframe[dataframe['name'] == protein['name']]

            for column_name in protein:
                if db_protein[column_name].iloc[0] != protein[column_name]:
                    app_logger.warning('Failed checking column \'%s\' of multidata/protein with name \'%s\'' % (
                        column_name, protein['name']))
                    app_logger.warning('Expected value: %s' % protein[column_name])
                    app_logger.warning('Database value: %s' % db_protein[column_name].iloc[0])
                    app_logger.warning('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some proteins doesnt match')

    def test_complex_composition_table(self):
        df_multidata = cellphonedb_app.cellphonedb.database_manager.get_repository('multidata').get_all()
        df_complex_composition = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'complex').get_all_compositions()

        number_compositions_not_match = False
        some_protein_didnt_exists = False
        some_protein_not_part_of_complex = False

        for complex in complex_entries:
            db_complex_id = df_multidata[df_multidata['name'] == complex['data']['name']]['id_multidata'].iloc[0]

            if len(df_complex_composition[df_complex_composition['complex_multidata_id'] != db_complex_id]) == len(
                    complex['composition']):
                app_logger.warning('Failed checking number of complex_composition with name \'%s\'' % (
                    complex['data']['name']))
                app_logger.warning('Expected value: %s' % len(
                    df_complex_composition[df_complex_composition['complex_multidata_id'] == db_complex_id]))
                app_logger.warning('Database value: %s' % len(complex['composition']))
                app_logger.warning('---')
                number_compositions_not_match = True

            for protein_name in complex['composition']:
                db_complex_composition_ids = \
                    df_complex_composition[df_complex_composition['complex_multidata_id'] == db_complex_id][
                        'protein_multidata_id'].tolist()

                composition_multidata_id = df_multidata[df_multidata['name'] == protein_name]['id_multidata']

                if not len(composition_multidata_id):
                    app_logger.warning('Failed finding protein \'%s\' in multidata from complex name \'%s\'' % (
                        protein_name, complex['data']['name']))
                    some_protein_didnt_exists = True
                    continue

                if composition_multidata_id.iloc[0] not in db_complex_composition_ids:
                    app_logger.warning('Failed finding protein \'%s\' in composition from complex name \'%s\'' % (
                        protein_name, complex['data']['name']))
                    some_protein_not_part_of_complex = True

        self.assertFalse(number_compositions_not_match, 'Number of complex composition doesnt match')
        self.assertFalse(some_protein_didnt_exists, 'Some complex_composition proteins doesnt match')
        self.assertFalse(some_protein_not_part_of_complex, 'Complex_composition proteins doesnt match')

    def test_complex(self):

        dataframe = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'complex').get_all_expanded()

        data_not_match = False

        for complex in complex_entries:
            db_complex = dataframe[dataframe['name'] == complex['data']['name']]

            for complex_data in complex['data']:
                if db_complex[complex_data].iloc[0] != complex['data'][complex_data]:
                    app_logger.warning('Failed checking column \'%s\' of multidata/complex with name \'%s\'' % (
                        complex_data, complex['data']['name']))
                    app_logger.warning('Expected value: %s' % complex['data'][complex_data])
                    app_logger.warning('Database value: %s' % db_complex[complex_data].iloc[0])
                    app_logger.warning('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some complex doesnt match')

    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def setUp(self):
        self.client = self.app.test_client()
