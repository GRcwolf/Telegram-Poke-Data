from poke_api import PokeApi
import telegram
import poke_utils


def main():
    poke_api = PokeApi()
    # Update the list of subscribers.
    telegram.update_subscriptions()
    # Map image captions
    image_dictionary = {'back_default': 'Back',
                        'back_shiny': 'Back Shiny',
                        'front_default': 'Front',
                        'front_shiny': 'Front Shiny',
                        'back_female': 'Female Back',
                        'back_shiny_female': 'Female Back Shiny',
                        'front_female': 'Female Front',
                        'front_shiny_female': 'Female Front Shiny'}

    # Get a random Pokemon.
    pokemon = poke_api.get_random_pokemon()
    for image in pokemon['sprites']:
        # Load the name of the image.
        image_name = '<strong>' + pokemon['name'] + ':</strong> ' + image_dictionary[image]
        # Send the image to the subscribed users.
        telegram.send_image(pokemon['sprites'][image], image_name, 'HTML', True)
    # Generate the message body.
    message = '<strong>' + pokemon['name'] + '</strong>' +\
              "\n" + '-------------------------' +\
              "\n" + '<b>Order:</b> ' + str(pokemon['order']) +\
              "\n" + '<b>Height:</b> ' + str(pokemon['height']) +\
              "\n" + '<b>Weight:</b> ' + str(pokemon['weight']) +\
              "\n" + '<b>Abilities:</b> ' + ', '.join(poke_utils.get_abilities(pokemon)) +\
              "\n" + '<b>Moves:</b> ' + ', '.join(poke_utils.get_moves_with_link(pokemon))
    # Send the message to the subscribed users.
    telegram.send_message(message, 'HTML')


if __name__ == '__main__':
    main()
