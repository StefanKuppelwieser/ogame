import time
import random

from loguru import logger
from datetime import datetime, timedelta
from ogame import OGame
from ogame.constants import mission, ships, coordinates


class Expedition(object):
    def __init__(self, properties, empire, telegram, utils):
        self.properties = properties
        self.empire: OGame = empire
        self.telegram = telegram
        self.utils = utils

    def get_current_expeditions(self):
        current_fleets = self.empire.friendly_fleet()
        expeditions_count = 0

        for fleet in current_fleets:
            if fleet.mission == mission.expedition:
                expeditions_count += 1

        return expeditions_count

    def check_free_expedition_slots(self):
        while self.properties.get_amount_expeditions_fleets() <= self.get_current_expeditions() or \
                len(self.empire.friendly_fleet()) >= self.properties.get_amount_max_fleets():
            message = 'Currently are {0} of {1} of expeditions and {3} of {4} fleets on the way. Wait {2} for next ' \
                      'try..'.format(
                self.get_current_expeditions(),
                self.properties.get_amount_expeditions_fleets(),
                self.properties.EXPEDITIONS_RECHECK,
                len(self.empire.friendly_fleet()),
                self.properties.get_amount_max_fleets()
            )
            logger.info(message)
            #self.telegram.send_message(message)
            time.sleep(self.properties.EXPEDITIONS_RECHECK)

    def build_pathfinder(self, planet_id, amount=1):
        if self.empire.ships(planet_id).explorer.amount == 0:
            message = 'Build ship of type explorer on planet {0}'.format(planet_id)
            logger.info(message)
            self.telegram.send_message(message)
            self.empire.build(ships.explorer(amount), planet_id)

            waiting_time_to_break = 30
            waiting_time = 60
            now_plus = datetime.now() + timedelta(minutes=waiting_time_to_break)

            while self.empire.ships(planet_id).explorer.amount > 0:
                if now_plus < datetime.now():
                    message = 'Break to wait of a new pathfinder. Continue without pathfinder'
                    logger.info(message)
                    break

                message = 'Wait 4 finishing to build a ship of type explorer is build up on planet {0}. Wait {1} seconds'.format(
                    planet_id,
                    waiting_time
                )
                logger.info(message)
                time.sleep(waiting_time)

    def build_probe(self, planet_id, amount=1):
        if self.empire.ships(planet_id).espionage_probe.amount == 0:
            message = 'Build ship of type probe on planet {0}'.format(planet_id)
            logger.info(message)
            self.telegram.send_message(message)
            self.empire.build(ships.espionage_probe(amount), planet_id)

            while self.empire.ships(planet_id).espionage_probe.amount > 0:
                waiting_time = 30
                message = 'Wait 4 finishing to build a ship of type explorer is build up on planet {0}. Wait {1} seconds'.format(
                    planet_id,
                    waiting_time
                )
                time.sleep(waiting_time)

    def get_amount_battleships(self, planet_id):
        class Amount:
            amount_reaper = 0
            skip = False
            if self.empire.ships(planet_id).reaper.amount > 0:
                amount_reaper = 1
                skip = True

            amount_bomber = 0
            if amount_reaper > 0:
                pass
            elif self.empire.ships(planet_id).bomber.amount > 0 and skip == False:
                amount_bomber = 1
                skip = True

            amount_interceptor = 0
            if amount_bomber > 0:
                pass
            elif self.empire.ships(planet_id).interceptor.amount > 0 and skip == False:
                amount_interceptor = 1
                skip = True

            amount_reaper = 0
            if amount_interceptor > 0:
                pass
            elif self.empire.ships(planet_id).reaper.amount > 0 and skip == False:
                amount_reaper = 1
                skip = True

            amount_battleship = 0
            if amount_reaper > 0:
                pass
            elif self.empire.ships(planet_id).battleship.amount > 0 and skip == False:
                amount_battleship = 1
                skip = True

            amount_cruiser = 0
            if amount_battleship > 0:
                pass
            elif self.empire.ships(planet_id).cruiser.amount > 0 and skip == False:
                amount_cruiser = 1
                skip = True

            amount_heavy_figther = 0
            if amount_cruiser > 0:
                pass
            elif self.empire.ships(planet_id).heavy_fighter.amount > 0 and skip == False:
                heavy_fighter = 1
                skip = True

            amount_light_fighter = 0
            if amount_heavy_figther > 0:
                pass
            elif self.empire.ships(planet_id).light_fighter.amount > 0 and skip == False:
                amount_light_fighter = 1
                skip = True

        return Amount

    def get_amount_cargos(self, planet_id):
        amount_large_cargos = self.empire.ships(planet_id).large_transporter.amount
        amount_small_cargos = self.empire.ships(planet_id).small_transporter.amount

        if self.properties.EXPEDITIONS_LARGE_CARGOS <= amount_large_cargos:
            if amount_large_cargos > 1340:
                amount_large_cargos = 1340
            amount_small_cargos = 0
            #amount_large_cargos = self.properties.EXPEDITIONS_LARGE_CARGOS
        elif self.properties.EXPEDITIONS_SMALL_CARGOS <= amount_small_cargos:
            amount_large_cargos = 0
            #amount_small_cargos = self.properties.EXPEDITIONS_SMALL_CARGOS
        else:
            # take current amount of ships
            pass

        class Cargos:
            large_cargos = amount_large_cargos
            small_cargos = amount_small_cargos
            total_space = amount_large_cargos * self.properties.PROBES_LARGE_CARGOS + amount_small_cargos * self.properties.PROBES_SMALL_CARGOS

        return Cargos

    def auto_run_expedition(self):

        while True:
            tmp_space = 0
            tmp_source_planet = None
            tmp_cargos = None

            # check free slot
            self.check_free_expedition_slots()

            # get best cords for expedition
            for planet in self.empire.all_planet_ids():
                # get cargos
                cargos = self.get_amount_cargos(planet)

                # choice planet
                if tmp_space <= cargos.total_space:
                    tmp_cargos = cargos
                    tmp_space = cargos.total_space
                    tmp_source_planet = planet

            # get amount battleships
            battleships = self.get_amount_battleships(tmp_source_planet)

            # check pathfinder
            # self.build_pathfinder(tmp_source_planet)

            # build probe
            self.build_probe(tmp_source_planet)

            # send fleet
            try:
                target = coordinates(
                    self.empire.celestial_coordinates(tmp_source_planet)[0],
                    int(self.empire.celestial_coordinates(tmp_source_planet)[1] + random.uniform(-10, 10)),
                    16)

                response = self.empire.send_fleet(
                    mission=mission.expedition,
                    id=tmp_source_planet,
                    where=target,
                    ships=[
                        ships.explorer(1),
                        ships.espionage_probe(1),
                        ships.large_transporter(tmp_cargos.large_cargos),
                        ships.small_transporter(tmp_cargos.small_cargos),
                        ships.reaper(battleships.amount_reaper),
                        ships.bomber(battleships.amount_bomber),
                        ships.interceptor(battleships.amount_interceptor),
                        ships.battleship(battleships.amount_battleship),
                        ships.cruiser(battleships.amount_cruiser),
                        ships.heavy_fighter(battleships.amount_heavy_figther),
                        ships.light_fighter(battleships.amount_light_fighter)
                    ],
                    holdingtime=1)
            except:
                logger.error('Error during send fleets in auto_run_expedition')
                continue
            if response:
                message = 'Send {0} large and {1} small cargos from {2} to explore {3}'.format(
                    tmp_cargos.large_cargos,
                    tmp_cargos.small_cargos,
                    self.empire.celestial_coordinates(tmp_source_planet),
                    target
                )
                logger.info(message)
                self.telegram.send_message(message)
            else:
                logger.debug('Something went wrong on planet {0}. Can not send a fleet to explore'.format(
                    self.empire.celestial_coordinates(tmp_source_planet)))
