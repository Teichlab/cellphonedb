from cellcommdb.repository import interaction
from cellcommdb.repository.protein import get_protein_multidata_by_uniprot


# TODO: Get complexes
# TODO: Format result
# TODO: Extract methods
def call(receptor, min_score2):
    """

    :type receptor: str
    :type min_score2: float
    :rtype:
    """
    print('Get Ligands From Receptor')

    protein = get_protein_multidata_by_uniprot(receptor)

    if protein is None:
        raise Exception('Protein not found')

    if not _is_receptor(protein):
        raise Exception('This protein is not receptor')

    interactions = interaction.get_interactions_multidata_by_multidata_id(protein['id_protein'])
    interactions = filter_interactions_by_min_score2(interactions, min_score2)

    if interactions.empty:
        return interactions
    print(_filter_receptor_ligand_interactions_by_receptor(interactions, protein))


def filter_interactions_by_min_score2(interactions, min_score2):
    filtered_interactions = interactions[interactions['score_2'] > min_score2]

    return filtered_interactions


def _filter_receptor_ligand_interactions_by_receptor(interactions, receptor):
    """

    :type interactions: pd.DataFrame
    :type receptor: pd.Series
    :type ligand: pd.Series
    :rtype:
    """

    result = interactions[
        interactions.apply(lambda interaction: is_receptor_ligand_by_receptor(interaction, receptor), axis=1)]
    return result


def is_receptor_ligand_by_receptor(interaction, receptor):
    """

    :type interaction:
    :type receptor:
    :rtype:
    """

    if interaction['multidata_1_id'] == receptor['id_multidata'] \
            and is_ligand(interaction, suffix='_2'):
        return True

    if interaction['multidata_2_id'] == receptor['id_multidata'] \
            and is_ligand(interaction, suffix='_1'):
        return True

    return False


def is_ligand(protein, suffix=''):
    """

    :type protein: pd.Series
    :type is_ligand: str
    :rtype: bool
    """

    if protein['secretion%s' % suffix] == True \
            and protein['other%s' % suffix] == False:
        return True

    if protein['transmembrane%s' % suffix] == True \
            and protein['secretion%s' % suffix] == False \
            and protein['extracellular%s' % suffix] == True \
            and protein['cytoplasm%s' % suffix] == False \
            and protein['other%s' % suffix] == False \
            and protein['transporter%s' % suffix] == False:
        return True

    return False


def _is_receptor(protein):
    """

    :type protein: pd.Series
    :rtype: bool
    """
    if protein['receptor'] and protein['transmembrane']:
        return True

    return False
