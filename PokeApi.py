import requests
import math
from multiprocessing.dummy import Pool as ThreadPool
import random

# Constants
POKEMON_ENDPOINT = 'https://pokeapi.co/api/v2/pokemon/'


class PokeApi:
    def __init__(self):
        """
        Constructs a new PokeApi object.
        """
        self.pokemon = []

    def get_pokemon(self):
        """
        Loads all pokemon into a variable.

        :return:
        """
        if len(self.pokemon) > 0:
            return self.pokemon
        request_params = []
        response = requests.get(POKEMON_ENDPOINT, dict(limit=1)).json()
        total_count = response['count']
        # Check how many requests have to be made.
        total_requests = math.ceil(total_count / 20)
        [request_params.append(i) for i in range(0, total_requests)]
        pool = ThreadPool(16)
        # Make requests on multiple threads.
        pool.map(self.fetch_pokemon, request_params)
        return self.pokemon

    def fetch_pokemon(self, request):
        """
        Fetch a collection of pokemon by the request id.

        :param int request:
        """
        offset = request * 20
        pokemon_response = requests.get(POKEMON_ENDPOINT, dict(offset=offset)).json()
        # Save the pokemon in a variable.
        [self.pokemon.append(pokemon) for pokemon in pokemon_response['results']]

    def get_random_pokemon(self):
        """
        Returns a random pokemon.

        :return:
        """
        if len(self.pokemon) == 0:
            self.get_pokemon()
        poke_url = random.choice(self.pokemon)['url']
        return self.get_single_pokemon(poke_url)

    @staticmethod
    def get_single_pokemon(url):
        """
        Loads a single pokemon.

        :param str url:
        :return:
        """
        return requests.get(url).json()
