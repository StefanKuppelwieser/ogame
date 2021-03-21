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
                mission.park_ally,
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
                speed=1,
                holdingtime=0
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


    def save_ressources(self, planet_in_attack, planet_4_saving=None):
        # save ressources
        response = False
        resources = self.empire.resources(self.empire.id_by_planet_moon_cords(planet_in_attack))
        ships_to_save = self.empire.ships(self.empire.id_by_planet_moon_cords(planet_in_attack))

        if planet_4_saving is None:
            if planet_in_attack[3] == 3:
                planet_4_saving = planet_in_attack[:]
                planet_4_saving[3] = 1
            else:
                planet_4_saving = planet_in_attack[:]
                planet_4_saving[3] = 3
            pass

            # check if moon has transpoerts
            ## get all transporters
            ## wait

            while (resources.metal + resources.crystal + resources.deuterium) >= 50000:

                # define mission type
                total_ress = resources.metal + resources.crystal + resources.deuterium
                total_cargo_space = ships_to_save.small_transporter.amount * self.properties.PROBES_SMALL_CARGOS\
                                    + ships_to_save.large_transporter.amount * self.properties.PROBES_LARGE_CARGOS
                mission_type = mission.transport
                metal = resources.metal
                crystal = resources.crystal
                deuterium = resources.deuterium

                if total_ress <= total_cargo_space:
                    mission_type = mission.park
                else:
                    # calculate space for resources
                    if total_cargo_space > resources.deuterium and resources.deuterium > 10000:
                        deuterium = resources.deuterium - 10000
                    if (total_cargo_space - deuterium) > resources.crystal:
                        crystal = resources.crystal
                    else:
                        crystal = total_cargo_space - deuterium
                    if (total_cargo_space - (deuterium + crystal)) > resources.metal:
                        metal = resources.metal
                    else:
                        metal = total_cargo_space - (deuterium + crystal)

                response = self.empire.send_fleet(
                    mission_type,
                    self.empire.id_by_planet_moon_cords(planet_in_attack),
                    planet_4_saving,
                    [
                        ships.small_transporter(ships_to_save.small_transporter.amount),
                        ships.large_transporter(ships_to_save.large_transporter.amount),
                    ],
                    resources=(metal, crystal, deuterium),
                )

                if response is True:
                    message = 'Send {0} small {1} large cargos with {2} metal, {3} crystal and {4} deut  from {5} {6} to {7} {8}. It are still {9} metal, {10} crystal and {11} deut'.format(
                        ships_to_save.small_transporter.amount,
                        ships_to_save.large_transporter.amount,
                        metal,
                        crystal,
                        deuterium,
                        planet_in_attack,
                        self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(planet_in_attack)),
                        planet_4_saving,
                        self.empire.name_by_planet_id(self.empire.id_by_planet_moon_cords(planet_4_saving)),
                        self.empire.resources(self.empire.id_by_planet_moon_cords(planet_in_attack)).metal,
                        self.empire.resources(self.empire.id_by_planet_moon_cords(planet_in_attack)).crystal,
                        self.empire.resources(self.empire.id_by_planet_moon_cords(planet_in_attack)).deuterium
                    )
                    logger.warning(message)
                    self.telegram.send_message(message)

                if mission_type != mission.park:
                    logger.info('Check if cargos are back for saving. Next run in {0} seconds.'.format('90'))
                    time.sleep(90)
                    resources = self.empire.resources(self.empire.id_by_planet_moon_cords(planet_in_attack))
                    ships_to_save = self.empire.ships(self.empire.id_by_planet_moon_cords(planet_in_attack))

        else:

            # define mission type
            total_ress = resources.metal + resources.crystal + resources.deuterium
            total_cargo_space = ships_to_save.small_transporter.amount * self.properties.PROBES_SMALL_CARGOS \
                                + ships_to_save.large_transporter.amount * self.properties.PROBES_LARGE_CARGOS
            metal = resources.metal
            crystal = resources.crystal
            deuterium = resources.deuterium

            # calculate space for resources
            if total_cargo_space > resources.deuterium:
                if resources.deuterium > 100000:
                    deuterium = (resources.deuterium - 100000) #-10000 4 fuel
                else:
                    deuterium = 0
            if (total_cargo_space - deuterium) > resources.crystal:
                crystal = resources.crystal
            else:
                crystal = total_cargo_space - deuterium
            if (total_cargo_space - (deuterium + crystal)) > resources.metal:
                metal = resources.metal
            else:
                metal = total_cargo_space - (deuterium + crystal)


            response = self.empire.send_fleet(
                mission.park_ally,
                self.empire.id_by_planet_moon_cords(planet_in_attack),
                planet_4_saving,
                [
                    ships.small_transporter(ships_to_save.small_transporter.amount),
                    ships.large_transporter(ships_to_save.large_transporter.amount),
                ],
                resources=(metal, crystal, deuterium),
                speed=1,
                holdingtime=0
            )

        if response is True:
            message = 'All cargos are saved! Send all ships from {0} {1} to {2} {3}'.format(
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
                    enemie_cache.diff = self.utils.get_diff_minutes(enemie_cache.arrival)
                    if enemie_cache.diff <= 11:
                        enemies_cache.remove(enemie_cache)

                # Add attack to cache list
                new_attacks = []
                for current_attack in self.empire.hostile_fleet():
                    # skip if it el_nappo aka President Neso
                    if current_attack.player_name == 'President Neso' and True:
                        continue
                    # skip if attack is under 12 minutes
                    current_attack.diff = self.utils.get_diff_minutes(current_attack.arrival)
                    if current_attack.diff <= 11:
                        continue
                    is_in_list = False
                    for old_attack in enemies_cache:
                        if old_attack.arrival == current_attack.arrival:
                            is_in_list = True
                    if is_in_list is False:
                        new_attacks.append(current_attack)

                # send message of new attacks
                for new_attack in new_attacks:
                    message = '!!! You are under attack from {0}, {2} at planet {3} {4}. He arrives at {5} in under {6} minutes !!!'.format(
                        new_attack.player_name,
                        new_attack.player_id,
                        new_attack.origin,
                        new_attack.destination,
                        self.empire.name_by_moon_planet_id(
                            self.empire.id_by_planet_moon_cords(new_attack.destination)),
                        new_attack.arrival,
                        new_attack.diff
                    )
                    logger.warning(message)
                    self.telegram.send_message(message)

                # add new attacks to cache
                enemies_cache.extend(new_attacks)

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
                for new_attack in enemies_cache:

                    if new_attack.destination[3] == 3:

                        # moon and planet are under attack. safe to elnappo
                        for enemy in enemies_cache:
                            if (new_attack.destination[0] == enemy.destination[0] and new_attack.destination[1] == enemy.destination[1] and new_attack.destination[2] == enemy.destination[2] and enemy.destination[3] == 1):
                                self.safe_battleships(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)
                                self.save_ressources(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)
                                break
                        else:
                            # check deut
                            if self.has_enough_deuterium(new_attack.destination):
                                pass
                            else:
                            #     # TODO: get deut of mother planet
                            #     pass
                            #
                                pass

                            self.safe_battleships(new_attack.destination)
                            self.save_ressources(new_attack.destination)

                    if new_attack.destination[3] == 1:

                        # moon and planet are under attack. safe to elnappo
                        for enemy in enemies_cache:
                            if (new_attack.destination[0] == enemy.destination[0] and new_attack.destination[1] == enemy.destination[1] and new_attack.destination[2] == enemy.destination[2] and enemy.destination[3] == 3):
                                self.safe_battleships(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)
                                self.save_ressources(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)
                                break
                        else:
                            has_planet_a_moon = self.has_planet_moon(new_attack.destination)

                            if has_planet_a_moon is True:
                                planet_4_saving = new_attack.destination[:]
                                planet_4_saving[3] = 3 #moon

                                self.safe_battleships(new_attack.destination)
                                self.save_ressources(new_attack.destination)
                            else:
                                self.safe_battleships(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)
                                self.save_ressources(new_attack.destination, self.properties.SAVING_PLANET_TO_SAVE)

            else:
                # reset list
                enemies_cache = []

            # wait for next check
            self.wait_for_next_run()
