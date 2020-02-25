def get_moves_with_link(pokemon):
    moves = []
    for move in pokemon['moves']:
        moves.append('<a href="' + move['move']['url'] + '">' + move['move']['name'] + '</a>')
    return moves
