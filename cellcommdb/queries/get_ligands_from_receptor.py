from cellcommdb.repository import interaction
from cellcommdb.repository.protein import get_protein_multidata_by_uniprot


def call(receptor):
    print('Get Ligands From Receptor')

    protein = get_protein_multidata_by_uniprot(receptor)

    if protein is None:
        raise Exception('Protein not found')

    if not _is_receptor(protein):
        raise Exception('This protein is not receptor')

    interaction.get_interactions_by_multidata_id(1)


def _is_receptor(protein):
    if protein['receptor'] and protein['transmembrane']:
        return True

    return False
