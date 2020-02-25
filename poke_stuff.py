from PokeApi import PokeApi
import telegram
import poke_utils


def main():
    poke_api = PokeApi()
    image_dictionary = {'back_default': 'Back',
                        'back_shiny': 'Back Shiny',
                        'front_default': 'Front',
                        'front_shiny': 'Front Shiny',
                        'back_female': 'Female Back',
                        'back_shiny_female': 'Female Back Shiny',
                        'front_female': 'Female Front',
                        'front_shiny_female': 'Female Front Shiny'}

    pokemon = poke_api.get_random_pokemon()
    for image in pokemon['sprites']:
        image_name = '<strong>' + pokemon['name'] + ':</strong> ' + image_dictionary[image]
        telegram.send_image(pokemon['sprites'][image], image_name, 'HTML', True)
    message = '<strong>' + pokemon['name'] + '</strong>' +\
              "\n" + '-------------------------' +\
              "\n" + '<b>Order:</b> ' + str(pokemon['order']) +\
              "\n" + '<b>Height:</b> ' + str(pokemon['height']) +\
              "\n" + '<b>Weight:</b> ' + str(pokemon['weight']) +\
              "\n" + '<b>Moves:</b> ' + ', '.join(poke_utils.get_moves_with_link(pokemon))
    telegram.send_message(message, 'HTML')


if __name__ == '__main__':
    main()
