from loguru import logger
from ogame import OGame
from telegram import Telegram
from datetime import datetime


def galaxy_distance(galaxy1, galaxy2, universe_size, donut_galaxy):
    if not donut_galaxy:
        return abs(20000 * round(galaxy2 - galaxy1))

    if galaxy1 > galaxy2:
        galaxy1, galaxy2 = galaxy2, galaxy1

    val = min(round(galaxy2 - galaxy1), round((galaxy1 + universe_size) - galaxy2))
    return 20000 * val


def system_distance(nb_systems, system1, system2, donut_system):
    if not donut_system:
        return abs(system2 - system1)

    if system1 > system2:
        system1, system2 = system2, system1

    val = min(round(system2 - system1), round((system1 + nb_systems) - system2))
    return val


# Returns the distance between two planets
def flight_system_distance(nbSystems, system1, system2, donut_system):
    return 2700 + 95 * system_distance(nbSystems, system1, system2, donut_system)


# Returns the distance between two planets
def planet_distance(planet1, planet2):
    return 1000 + 5 * abs(round(planet2 - planet1))


class Utils(object):
    def __init__(self, credentials_login, credentials_telgram):
        self.loginKey = credentials_login
        self.telegramKey = credentials_telgram

        self.telegram = Telegram(self.telegramKey.get('Token'), self.telegramKey.get('Chat'))
        message = 'Successfully registered in telegram'
        logger.info(message)
        self.telegram.send_message(message)

        self.empire = OGame(self.loginKey.get('Uni'), self.loginKey.get('Username'), self.loginKey.get('Password'),
                            self.telegram)
        message = 'Successfully registered in ogame'
        logger.info(message)
        self.telegram.send_message(message)

    ######################
    # Distance returns the distance between two coordinates
    ######################
    def distance(self, c1, c2, universe_size=6, nb_systems=499, donut_galaxy=True, donut_system=True):
        # prepare cords
        tmp = c2.replace('[', '')
        tmp = tmp.replace(']', '')
        tmp = tmp.split(':')
        c2 = []
        for cord in tmp:
            c2.append(int(cord))

        if c1[0] != c2[0]:
            return galaxy_distance(int(c1[0]), int(c2[0]), universe_size, donut_galaxy)
        if c1[1] != c2[1]:
            return flight_system_distance(nb_systems, int(c1[1]), int(c2[1]), donut_system)
        if c1[2] != c2[2]:
            return planet_distance(int(c1[2]), int(c2[2]))
        return 5

    def convertToCords(self, target_planet):
        cords = []
        target_planet = target_planet.replace('[', '')
        target_planet = target_planet.replace(']', '')
        for position in target_planet.split(':'):
            cords.append(int(position))
        return cords

    ######################
    # Time
    ######################
    def get_diff_minutes(self, datetime_before, datetime_after=datetime.now()):
        diff_minutes = 0
        seconds_in_day = 24 * 60 * 60

        divmod((datetime_after - datetime.now()).days * seconds_in_day + (datetime_after - datetime.now()).seconds, 60)[0]

        try:
            difference = datetime_before - datetime_after
            diff_minutes = divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]
        except:
            logger.error('Can not calculate the difference between two dateimes')
            return 0

        return diff_minutes
