import os

import pandas as pd

from tools.app import data_dir, output_dir


def remove_interactions_in_file(interaction_namefile, interactions_to_remove_namefile):
    if os.path.isfile('%s/%s' % (data_dir, interaction_namefile)):
        interactions_file = os.path.join(data_dir, interaction_namefile)
    else:
        interactions_file = os.path.join(output_dir, interaction_namefile)

    interactions_df = pd.read_csv(interactions_file)
    interactions_remove_df = pd.read_csv('%s/%s' % (data_dir, interactions_to_remove_namefile))

    def interaction_not_exists(row):
        if len(interactions_remove_df[(row['protein_1'] == interactions_remove_df['protein_1']) & (
                    row['protein_2'] == interactions_remove_df['protein_2'])]):
            return False

        if len(interactions_remove_df[(row['protein_1'] == interactions_remove_df['protein_2']) & (
                    row['protein_2'] == interactions_remove_df['protein_1'])]):
            return False

        return True

    interactions_filtered = interactions_df[interactions_df.apply(interaction_not_exists, axis=1)]

    interactions_filtered.to_csv('%s/clean_interactions.csv' % (output_dir), index=False)
