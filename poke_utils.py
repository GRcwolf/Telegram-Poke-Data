def get_moves_with_link(pokemon):
    """
    Gets an HTML a tag that links to the api path for the move.

    :param pokemon:
    :return:
    """
    moves = []
    for move in pokemon['moves']:
        moves.append('<a href="' + move['move']['url'] + '">' + move['move']['name'] + '</a>')
    return moves


def get_abilities(pokemon):
    """
    Returns a list of the pokemon's abilities.

    :param pokemon:
    :rtype: list
    """
    abilities = []
    for ability in pokemon['abilities']:
        abilities.append(ability['ability']['name'])
    return abilities
