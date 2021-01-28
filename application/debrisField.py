import time

from loguru import logger
from ogame import OGame
from ogame.constants import mission, ships, coordinates, destination


class DebrisField(object):
    def __init__(self, properties, empire, telegram, utils):
        self.properties = properties
        self.empire: OGame = empire
        self.telegram = telegram
        self.utils = utils


    def wait_for_next_run(self):
        time.sleep(self.properties.DEBRIS_RECHECK)
        logger.info('Wait {0} for next run to check the debris fields'.format(self.properties.DEBRIS_RECHECK))


    def collect_debris_planet_infos(self):
        message = "Get debris, planets and moons"
        logger.info(message)

        planets_scanned = []
        for current_planet in self.empire.planet_ids():
            cords = self.empire.celestial_coordinates(current_planet)
            planets_scanned.extend(tmp_planets_scanned for tmp_planets_scanned in self.empire.galaxy(coordinates(cords[0], cords[1])) if tmp_planets_scanned.position == cords)

        return planets_scanned

    def send_rececyler(self, source_planet_id, amount_recycler):
        cords = self.empire.celestial_coordinates(source_planet_id)
        target = coordinates(cords[0], cords[1], cords[2], destination.debris)

        response = self.empire.send_fleet(
            mission=mission.recycle,
            id=source_planet_id,
            where=target,
            ships=[
                ships.recycler(amount_recycler),
            ])

        if response:
            message = 'Send {0} recycler from {1} to loot debris at {2}'.format(
                amount_recycler,
                cords,
                target
            )
            logger.info(message)
            self.telegram.send_message(message)

    def check_free_fleet_slots(self):
        while len(self.empire.friendly_fleet()) <= self.properties.get_amount_max_fleets():
            message = 'Currently are {0} of {1} fleets occupied. Wait {2} for next try..'.format(
                len(self.empire.friendly_fleet()),
                self.properties.get_amount_max_fleets(),
                self.properties.DEBRIS_RECHECK,
            )
            logger.info(message)
            # self.telegram.send_message(message)
            time.sleep(self.properties.DEBRIS_RECHECK)

    def auto_collect_debris_fields(self):

        while True:
            self.check_free_fleet_slots()
            try:
                scanned_planets = self.collect_debris_planet_infos()

                # iterate all systems
                for scanned_planet in scanned_planets:

                    # debris exist
                    if scanned_planet.debris is True:
                        planet_id = self.empire.id_by_planet_name(scanned_planet.name)
                        ships = self.empire.ships(planet_id)

                        # send fleets from planet
                        if ships.recycler.amount > 0:
                            self.send_rececyler(planet_id, ships.recycler.amount)
                        # send fleets from planet
                        elif scanned_planet.moon is True:
                            moon_id = self.empire.id_by_moon_name(scanned_planet.moon_name)
                            ships = self.empire.ships(moon_id)
                            if ships.recycler.amount > 0:
                                self.send_rececyler(moon_id, ships.recycler.amount)
                            else:
                                message = 'No recycler on planet {0} and moon {1} to loot debris'.format(scanned_planet.name, scanned_planet.moon_name)
                                logger.info(message)
                                #self.telegram.send_message(message)
                        else:
                            message = 'No recycler on planet {0} to loot debris'.format(scanned_planet.name)
                            logger.info(message)
                            #self.telegram.send_message(message)
            except:
                logger.error('An error occurred in auto_collect_debris_fields(). Restart auto_collect_debris_fields()')

            # wait for next check
            self.wait_for_next_run()