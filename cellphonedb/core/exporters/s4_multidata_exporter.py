import pandas as pd


def call(multidatas_expanded: pd.DataFrame):
    return multidatas_expanded[
        ['name', 'entry_name', 'transmembrane', 'secretion', 'peripheral', 'is_cellphone_receptor',
         'is_cellphone_ligand', 'integrin_interaction', 'secreted_highlight', 'secreted_desc', 'transporter', 'other',
         'other_desc', 'tags', 'tags_description', 'tags_reason']]
