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
