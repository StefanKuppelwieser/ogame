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

    def safe_battleships(self, attacked_planet):
        ships_to_save = self.empire.ships(self.empire.id_by_planet_moon_cords(attacked_planet))

        park_planet = None
        if attacked_planet[3] == 3:
            park_planet = attacked_planet[:]
            park_planet[3] = 1
        else:
            park_planet = attacked_planet[:]
            park_planet[3] = 3

        response = self.empire.send_fleet(
            self.empire.id_by_planet_moon_cords(attacked_planet),
            self.empire.id_by_planet_moon_cords(park_planet),
            [
                ships.light_fighter(ships_to_save.light_fighter.amount),
                ships.heavy_fighter(ships_to_save.heavy_fighter.amount),
                ships.cruiser(ships_to_save.cruiser.amount),
                ships.battleship(ships_to_save.battleship.amount),
                ships.interceptor(ships_to_save.interceptor.amount),
                ships.bomber(ships_to_save.bomber.amount),
                ships.destroyer(ships_to_save.destroyer.amount),
                ships.deathstar(ships_to_save.deathstar.amount),
                ships.explorer(ships_to_save.explorer.amount),
                ships.colonyShip(ships_to_save.colonyShip.amount),
                ships.recycler(ships_to_save.recycler.amount),
                ships.espionage_probe(ships_to_save.espionage_probe.amount),
            ]
        )

        if response is True:
            message = 'All battleships are saved! Send all ships from {0} {1} to {2} {3}'.format(
                attacked_planet,
                self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(attacked_planet)),
                park_planet,
                self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(park_planet))
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
                planet_to_save = [3, 162, 4, 1] #Thx to PResident Neso
                for new_attack in new_attacks:

                    if new_attack.destination[3] == 3:

                        # check deut
                        if self.has_enough_deuterium(new_attack.destination):
                            pass
                        else:
                        #     # TODO: get deut of mother planet
                        #     pass
                        #
                            pass

                        ## safe battleships
                        #self.safe_battleships(new_attack.destination)

                        # # save from moon to planet
                        #     # safe battle ships
                        #     # safe ressources

                    if new_attack.destination[3] == 1:
                        has_planet_a_moon = self.has_planet_moon(new_attack.destination)
                        #safe from planet to moon
                            # safe battle ships
                            # safe ressources
                        # ELSE
                            # safe to elnappo
                            # safe battle ships
                            # safe ressources
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
