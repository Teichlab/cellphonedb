import os

import pandas as pd

from tools.app import data_dir, output_dir


def remove_interactions_in_file(interactions, interactions_to_remove):
    def interaction_not_exists(row):
        if len(interactions_to_remove[(row['protein_1'] == interactions_to_remove['protein_1']) & (
                    row['protein_2'] == interactions_to_remove['protein_2'])]):
            return False

        if len(interactions_to_remove[(row['protein_1'] == interactions_to_remove['protein_2']) & (
                    row['protein_2'] == interactions_to_remove['protein_1'])]):
            return False

        return True

    interactions_filtered = interactions[interactions.apply(interaction_not_exists, axis=1)]

    return interactions_filtered
