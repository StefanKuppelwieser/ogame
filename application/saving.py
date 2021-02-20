import time

from ogame import OGame
from loguru import logger

from ogame.constants import coordinates, status, ships, mission

class Saving(object):
    def __init__(self, properties, empire, telegram, utils):
        self.properties = properties
        self.empire: OGame = empire
        self.telegram = telegram
        self.utils = utils

    def wait_for_next_run(self):
        logger.info('Check if you get attacked or not. Next run in {0} seconds.'.format(self.properties.SAVING_RECHECK_ATTACKS))
        time.sleep(self.properties.SAVING_RECHECK_ATTACKS)

    def has_planet_moon(self, target):
        planets_scanned = []
        for current_planet in self.empire.planet_ids():
            cords = self.empire.celestial_coordinates(current_planet)
            planets_scanned.extend(tmp_planets_scanned for tmp_planets_scanned in self.empire.galaxy(coordinates(cords[0], cords[1])) if tmp_planets_scanned.position == cords and tmp_planets_scanned.moon is True)

        for planet_scanned in planets_scanned:
            if planet_scanned.position == target:
                return planet_scanned.moon
        return False

    def has_enough_deuterium(self, source_planet):
        if self.empire.resources(source_planet).deuterium >= 20000:
            return True
        message = 'Not enough deuterium on planet {0} {1} to safe fleets or ressources'.format(
            source_planet,
            self.empire.name_by_moon_planet_id(source_planet)
        )
        logger.info(message)
        self.telegram.send_message(message)
        return False

    def safe_battleships(self, planet_in_attack, planet_4_saving=None):
        ships_to_save = self.empire.ships(self.empire.id_by_planet_moon_cords(planet_in_attack))#
        response = False

        if planet_4_saving is None:
            if planet_in_attack[3] == 3:
                planet_4_saving = planet_in_attack[:]
                planet_4_saving[3] = 1
            else:
                planet_4_saving = planet_in_attack[:]
                planet_4_saving[3] = 3

            response = self.empire.send_fleet(
                mission.park,
                self.empire.id_by_planet_moon_cords(planet_in_attack),
                planet_4_saving,
                [
                    ships.light_fighter(ships_to_save.light_fighter.amount),
                    ships.heavy_fighter(ships_to_save.heavy_fighter.amount),
                    ships.cruiser(ships_to_save.cruiser.amount),
                    ships.battleship(ships_to_save.battleship.amount),
                    ships.interceptor(ships_to_save.interceptor.amount),
                    ships.bomber(ships_to_save.bomber.amount),
                    ships.destroyer(ships_to_save.destroyer.amount),
                    ships.deathstar(ships_to_save.deathstar.amount),
                    ships.reaper(ships_to_save.reaper.amount),
                    ships.explorer(ships_to_save.explorer.amount),
                    ships.colonyShip(ships_to_save.colonyShip.amount),
                    ships.recycler(ships_to_save.recycler.amount),
                    ships.espionage_probe(ships_to_save.espionage_probe.amount),
                ]
            )
        else:
            response = self.empire.send_fleet(
                mission.transport,
                self.empire.id_by_planet_moon_cords(planet_in_attack),
                planet_4_saving,
                [
                    ships.light_fighter(ships_to_save.light_fighter.amount),
                    ships.heavy_fighter(ships_to_save.heavy_fighter.amount),
                    ships.cruiser(ships_to_save.cruiser.amount),
                    ships.battleship(ships_to_save.battleship.amount),
                    ships.interceptor(ships_to_save.interceptor.amount),
                    ships.bomber(ships_to_save.bomber.amount),
                    ships.destroyer(ships_to_save.destroyer.amount),
                    ships.deathstar(ships_to_save.deathstar.amount),
                    ships.reaper(ships_to_save.reaper.amount),
                    ships.explorer(ships_to_save.explorer.amount),
                    ships.colonyShip(ships_to_save.colonyShip.amount),
                    ships.recycler(ships_to_save.recycler.amount),
                    ships.espionage_probe(ships_to_save.espionage_probe.amount),
                ],
                speed=1
            )

        if response is True:
            message = 'All battleships are saved! Send all ships from {0} {1} to {2} {3}'.format(
                planet_in_attack,
                self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(planet_in_attack)),
                planet_4_saving,
                self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(planet_4_saving))
            )
            logger.warning(message)
            self.telegram.send_message(message)

    def auto_run_saving(self):

        enemies_cache = []

        while True:
            # check if you get attacked
            if self.empire.attacked():

                # Reduce list
                for enemie_cache in enemies_cache:
                    diff = self.utils.get_diff_minutes(enemie_cache.arrival)
                    if diff < int(self.properties.SAVING_RECHECK_ATTACKS / 60):
                        enemies_cache.remove(enemie_cache)

                # Add attack to cache list
                new_attacks = []
                for current_attack in self.empire.hostile_fleet():
                    # skip if attack is under 5 minutes
                    diff = self.utils.get_diff_minutes(current_attack.arrival)
                    if diff <= 10:
                        continue
                    is_in_list = False
                    for old_attack in enemies_cache:
                        if old_attack.arrival == current_attack.arrival:
                            is_in_list = True
                    if is_in_list is False:
                        new_attacks.append(current_attack)

                # send message of new attacks
                for new_attack in new_attacks:
                    message = '!!! You are under attack from {0}, {2} at planet {3} {4}. He arrives at {5} !!!'.format(
                        new_attack.player_name,
                        new_attack.player_id,
                        new_attack.origin,
                        new_attack.destination,
                        self.empire.name_by_moon_planet_id(
                            self.empire.id_by_planet_moon_cords(new_attack.destination)),
                        new_attack.arrival
                    )
                    logger.warning(message)
                    self.telegram.send_message(message)

                # # send probe
                # if self.empire.send_fleet(mission.spy, self.empire.id_by_planet_moon_cords(new_attack.destination), new_attack.origin, [ships.espionage_probe(self.properties.SAVING_SEND_PROBES)]):
                #     # get information about last spy
                #     fleet = reversed(self.empire.friendly_fleet()).list[1]
                #     if fleet == mission.spy:
                #         message = 'You get attack. Send {2} probes to planet {0}. The probe arrives at {1}' \
                #                   'list'.format(
                #             fleet.destination,
                #             fleet.arrival,
                #             self.properties.SAVING_SEND_PROBES
                #         )
                #         logger.info(message)
                #         self.telegram.send_message(message)
                #         continue

                # check if planet has a moon or planet
                for new_attack in new_attacks:

                    if new_attack.destination[3] == 3 and False:

                        # check deut
                        if self.has_enough_deuterium(new_attack.destination):
                            pass
                        else:
                        #     # TODO: get deut of mother planet
                        #     pass
                        #
                            pass

                        # safe battleships
                        self.safe_battleships(new_attack.destination)

                    if new_attack.destination[3] == 1:
                        has_planet_a_moon = self.has_planet_moon(new_attack.destination)

                        if has_planet_a_moon is True:
                            planet_4_saving = new_attack.destination[:]
                            planet_4_saving[3] = 3 #moon

                            self.safe_battleships(new_attack.destination)
                        else:
                            self.safe_battleships(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)

                        # safe resources
                        pass

                # save ressources

                    # Nachricht raus an Telegram mit start des savens
                    # checken ob der planet/mond einen mond/planet hat
                    # Alle transporter holen
                    # Todestern einzeln an den anderen planeten senden
                    # Alle Flotten an den planeten senden. Voll machen mit metall, dann kristall, dann deut
                    # while aller Transporter
                        # Alle resourcen schicken
                        # beim letzten loop transport stationieren statt transport
                    # complett gesaved
                    # Nachricht an Telegram raus


                # add new attacks to cache
                enemies_cache.extend(new_attacks)

            else:
                # reset list
                enemies_cache = []

            # wait for next check
            #self.wait_for_next_run()
