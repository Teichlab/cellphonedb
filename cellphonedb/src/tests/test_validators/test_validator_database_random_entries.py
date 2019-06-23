import pandas as pd
from flask_testing import TestCase

from cellphonedb.src.app.cellphonedb_app import cellphonedb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.flask.flask_app import create_app

complex_entries = [
    {
        'data': {
            "name": "aVb3 complex",
            "transmembrane": True,
            "peripheral": False,
            "secreted": False,
            "secreted_desc": None,
            "secreted_highlight": False,
            "receptor": False,
            "receptor_desc": None,
            "integrin": True,
            "other": False,
            "other_desc": None,
            "pdb_id": "1jv2",
            "pdb_structure": "TRUE",
            "stoichiometry": "ITGAV;ITGB3",
            "comments_complex": "Well known integrin combination"
        },
        'composition': ["P06756", "P05106"]
    },
    {
        'data': {
            "name": "a2Bb3 complex",
            "receptor": False,
            "receptor_desc": None,
            "other": False,
            "other_desc": None,
            "secreted_highlight": False,
            "secreted_desc": None,
            "transmembrane": True,
            "secreted": False,
            "peripheral": False,
            "pdb_structure": "TRUE",
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
            "name": "IL2 receptor_HA",
            "transmembrane": True,
            "peripheral": False,
            "secreted": False,
            "secreted_desc": None,
            "secreted_highlight": False,
            "receptor": True,
            "receptor_desc": "Cytokine receptor IL2 family",
            "integrin": False,
            "other": False,
            "other_desc": None,
            "pdb_id": "2b5i",
            "pdb_structure": "binding",
            "stoichiometry": "IL2;IL2RA;IL2RB;IL2RG",
            "comments_complex": "A high affinity dimer, an intermediate affinity monomer (beta subunit). The high and intermediate affinity forms also associate with a gamma subunit."
        },
        'composition':
            ["P01589", "P14784", "P31785"]
    }
]
protein_entries = [
    {
        "name": "P39019",
        "protein_name": "RS19_HUMAN",
        "transmembrane": False,
        "peripheral": False,
        "secreted": False,
        "secreted_desc": None,
        "secreted_highlight": False,
        "receptor": False,
        "receptor_desc": None,
        "integrin": False,
        "other": False,
        "other_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": None,

    }, {

        "name": "P54760",
        "protein_name": "EPHB4_HUMAN",
        "transmembrane": True,
        "peripheral": False,
        "secreted": False,
        "secreted_desc": None,
        "secreted_highlight": False,
        "receptor": True,
        "receptor_desc": None,
        "integrin": False,
        "other": False,
        "other_desc": None,
        "tags": "To_comment",
        "tags_reason": "Adhesion_add",
        "tags_description": None

    }, {
        "name": "P52799",
        "protein_name": "EFNB2_HUMAN",
        "transmembrane": True,
        "peripheral": False,
        "secreted": False,
        "secreted_desc": None,
        "secreted_highlight": False,
        "receptor": True,
        "receptor_desc": None,
        "integrin": False,
        "other": False,
        "other_desc": None,
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "ligandIUPHAR",
    },
    {
        "name": "P39059",
        "protein_name": "COFA1_HUMAN",
        "transmembrane": False,
        "peripheral": False,
        "secreted": True,
        "secreted_desc": None,
        "secreted_highlight": False,
        "receptor": False,
        "receptor_desc": None,
        "integrin": False,
        "other": True,
        "other_desc": "Collagen",
        "tags": "To_add",
        "tags_reason": None,
        "tags_description": "Collagen"
    },
]
gene_entries = [
    {
        "ensembl": "ENSG00000275555",
        "gene_name": "DLL1",
        "name": "O00548"
    },
    {
        "ensembl": "ENSG00000169306",
        "gene_name": "IL1RAPL1",
        "name": "Q9NZN1"
    },
    {
        "ensembl": "ENSG00000204642",
        "gene_name": "HLA-F",
        "name": "P30511"
    }
]
interaction_entries = [
    {
        "id_cp_interaction": "CPI-CS0A66DB1CA",
        "name_1": "CD8 receptor",
        "name_2": "P06239",
        "source": "1q69, PDB partially",
        "annotation_strategy": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS085EE60B1",
        "name_1": "P01137",
        "name_2": "Q03167",
        "source": "uniprot",
        "annotation_strategy": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS056BE1011",
        "name_1": "O00421",
        "name_2": "Q99731",
        "source": None,
        "annotation_strategy": "guidetopharmacology.org",
    },
    {
        "id_cp_interaction": "CPI-SS03165AD8C",
        "name_1": "O00590",
        "name_2": "P13500",
        "source": "PMID: 24218476",
        "annotation_strategy": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS0F972435E",
        "name_1": "P35916",
        "name_2": "P49767",
        "source": "uniprot",
        "annotation_strategy": "curated",
    },
    {
        "id_cp_interaction": "CPI-SS027E57635",
        "name_1": "Q8NFJ6",
        "name_2": "Q9HC23",
        "annotation_strategy": "guidetopharmacology.org",
        "source": None
    },
    {
        "id_cp_interaction": "CPI-SS0DBA4D668",
        "name_1": "P27487",
        "name_2": "P48061",
        "annotation_strategy": "curated",
        "source": "PMID: 24218476"
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

            if db_protein.empty:
                print('Protein {} dindt exist'.format(protein['name']))
                data_not_match = True
                continue

            for column_name in protein:
                if db_protein[column_name].iloc[0] != protein[column_name]:
                    app_logger.warning('Failed checking column \'%s\' of multidata/protein with name \'%s\'' % (
                        column_name, protein['name']))
                    app_logger.warning('Expected value: %s' % protein[column_name])
                    app_logger.warning('Database value: %s' % db_protein[column_name].iloc[0])
                    app_logger.warning('---')
                    data_not_match = True

        self.assertFalse(data_not_match, 'Some proteins doesnt match or doesnt exist')

    def test_complex_composition_table(self):
        df_multidata = cellphonedb_app.cellphonedb.database_manager.get_repository('multidata').get_all()
        df_complex_composition = cellphonedb_app.cellphonedb.database_manager.get_repository(
            'complex').get_all_compositions()

        number_compositions_not_match = False
        some_protein_didnt_exists = False
        some_protein_not_part_of_complex = False
        some_complex_not_exist = False

        for complex in complex_entries:
            try:
                db_complex_id = df_multidata[df_multidata['name'] == complex['data']['name']]['id_multidata'].iloc[0]
            except IndexError:
                print('Complex {} didnt exist'.format(complex['data']['name']))
                some_complex_not_exist = True
                continue

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
        self.assertFalse(some_complex_not_exist, 'Some Complex not exist')

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
