from PokeApi import PokeApi
import telegram

if __name__ == '__main__':
    poke_api = PokeApi()
    pokemon = poke_api.get_random_pokemon()
    [telegram.send_image(pokemon['sprites'][image]) for image in pokemon['sprites']]
