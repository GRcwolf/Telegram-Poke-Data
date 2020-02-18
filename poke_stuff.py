from PokeApi import PokeApi

if __name__ == '__main__':
    poke_api = PokeApi()
    pokemon = poke_api.get_random_pokemon()
