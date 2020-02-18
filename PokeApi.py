import requests
import math
from multiprocessing.dummy import Pool as ThreadPool

# Constants
POKEMON_ENDPOINT = 'https://pokeapi.co/api/v2/pokemon'


class PokeApi:
    def __init__(self):
        self.pokemon = []

    def get_pokemon(self):
        if len(self.pokemon) > 0:
            return self.pokemon
        request_params = []
        response = requests.get(POKEMON_ENDPOINT, dict(limit=1)).json()
        total_count = response['count']
        total_requests = math.ceil(total_count / 20)
        [request_params.append(i) for i in range(0, total_requests)]
        pool = ThreadPool(16)
        pool.map(self.fetch_pokemon, request_params)
        return self.pokemon

    def fetch_pokemon(self, request):
        offset = request * 20
        pokemon_response = requests.get(POKEMON_ENDPOINT, dict(offset=offset)).json()
        [self.pokemon.append(pokemon) for pokemon in pokemon_response['results']]

    def get_random_pokemon(self):
