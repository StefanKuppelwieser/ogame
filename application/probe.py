import time
import math

from loguru import logger
from ogame.constants import coordinates, status, ships, mission


class Probe(object):
    def __init__(self, properties, empire, telegram, utils):
        self.properties = properties
        self.empire = empire
        self.telegram = telegram
        self.utils = utils

    def get_current_probes(self):
        current_fleets = self.empire.friendly_fleet()
        expeditions_count = 0

        for fleet in current_fleets:
            if fleet.mission == mission.attack or fleet.mission == mission.spy:
                expeditions_count += 1

        return expeditions_count

    def check_free_slots(self):
        while self.properties.get_amount_probe_fleets() <= self.get_current_probes() or \
                len(self.empire.friendly_fleet()) >= self.properties.get_amount_max_fleets():
            message = 'Currently are {0} of {1} of kind of spy or transport and {3} of {4} on the way. Wait {2} seconds for ' \
                      'next try..'.format(
                self.get_current_probes(),
                self.properties.get_amount_probe_fleets(),
                self.properties.PROBES_RECHECK,
                len(self.empire.friendly_fleet()),
                self.properties.get_amount_max_fleets()
            )
            logger.info(message)
            self.telegram.send_message(message)
            time.sleep(self.properties.EXPEDITIONS_RECHECK)


    ##################################
    # get inactive players           #
    ##################################
    def delete_spy_reports(self):
        self.empire.delete_all_spyreports()

        message = "All spy reports are deleted"
        logger.info(message)
        self.telegram.send_message(message)

    ##################################
    # get inactive players           #
    ##################################
    def get_inactive_planetsself(self):

        message = "Get inactive planets"
        logger.info(message)
        self.telegram.send_message(message)

        # Get inactive players
        planetsToCheck = []

        galaxy = int(self.properties.PROBES_GALAXY_RANGE[0])
        system = int(self.properties.PROBES_SYSTEM_RANGE[0])
        count = 1
        while self.properties.PROBES_GALAXY_RANGE[0] <= galaxy <= self.properties.PROBES_GALAXY_RANGE[1]:
            while self.properties.PROBES_SYSTEM_RANGE[0] <= system <= self.properties.PROBES_SYSTEM_RANGE[1]:
                for planet in self.empire.galaxy(coordinates(galaxy, system)):
                    try:
                        if (status.inactive in planet.status) and not (status.vacation in planet.status):
                            planetsToCheck.append(planet)
                            logger.info(
                                '#{3} at {2} has the status {1} and the name Planet {0}'.format(planet.name,
                                                                                                planet.status,
                                                                                                planet.position,
                                                                                                count))
                            count += 1
                    except:
                        logger.info('Error during find inactive planets. Try next system')
                system += 1
            system = int(self.properties.PROBES_SYSTEM_RANGE[0])  # reset system value
            galaxy += 1

        # filter blacklist
        result = [x for x in planetsToCheck if x not in self.properties.PROBES_BLACKLIST]

        # output message
        message = "Inactive scans are finished. Found {0} inactive planets on {1} galaxy".format(len(result),
                                                                                                 galaxy - 1)
        logger.info(message)
        self.telegram.send_message(message)
        return result

    ##################################
    # Send a spy probe to list       #
    ##################################
    def send_probes(self, planets):

        message = "Start to send probes to inactives planets"
        logger.info(message)
        self.telegram.send_message(message)

        # delete all spy reports
        if self.properties.PROBES_DELETE_OLD_SPY_REPORTS is True:
            self.delete_spy_reports()

        # revers list
        planets.reverse()

        # send probes
        while len(planets) > 0:
            # wait for free slots
            self.check_free_slots()

            # check if enough probs exist
            amount_of_probes = self.empire.ships(self.properties.get_source_planet()).espionage_probe.amount
            if amount_of_probes <= self.properties.PROBES_AMOUNT_OF_SONDES:
                # self.empire.build(ships.espionage_probe(send_amount_probes - amount_of_probes), planetBase)
                while self.empire.ships(
                        self.properties.get_source_planet()).espionage_probe.amount <= self.properties.PROBES_AMOUNT_OF_SONDES:
                    message = 'Not enough probs on the planet. Build new probs. Wait {0} seconds..'.format(
                        self.properties.EXPEDITIONS_DURATION
                    )
                    logger.info(message)
                    time.sleep(30)

            # send n probe
            try:
                if self.empire.send_fleet(mission.spy, self.properties.get_source_planet(), planets[-1].position,
                                          [ships.espionage_probe(self.properties.PROBES_AMOUNT_OF_SONDES)]):
                    # get information about last spy
                    for fleet in reversed(self.empire.friendly_fleet()):
                        if fleet.list[1] == mission.spy:
                            message = 'Mission SPYREPORT to {0} arrives at {1}. There are {2} planets left in the spy ' \
                                      'list'.format(fleet.destination, fleet.arrival, len(planets) - 1)
                            logger.info(message)
                            self.telegram.send_message(message)
                            planets = planets[:-1]
                            break
                else:
                    message = 'Something went wrong with spy probe at planet {0}. Planet skipped.'.format(
                        planets[-1].position)
                    logger.error(message)
                    self.telegram.send_message(message)
                    planets = planets[:-1]
            except:
                planets = planets[:-1]
                message = 'Code of spy probe crashed at planet {0}. Planet skipped.'.format(planets[-1].position)
                logger.error(message)
                self.telegram.send_message(message)

        message = 'Spy probes have done their jobs'
        logger.info(message)
        self.telegram.send_message('Spy probes have done their jobs')

    ##################################
    # log report                     #
    ##################################
    def print_report(self, lastPageSize):

        message = "print reports of all spy probes"
        logger.info(message)
        self.telegram.send_message(message)

        # wait all spys returns to base
        try:
            while True:
                send_fleets = 0
                for fleet in self.empire.friendly_fleet():
                    if fleet.list[1] == mission.spy:
                        send_fleets += 1
                if send_fleets > 0:
                    self.check_free_slots()
                else:
                    logger.warning('No spy fleets are on the planet. Start to get the spy report')
                    break
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            logger.error('Decoding JSON has failed in method print_report()')

        # get reports
        spyreports = sorted(self.empire.spyreports(lastpage=lastPageSize), key=lambda x: float(x.resourcesTotal),
                            reverse=True)  # sort list descending

        for spyreport in spyreports:
            message = '{3}: Total {7} Plunder {8} Metal {0} Crystal {1} Deuterium {2} Defense {6} ' \
                      '=> {9} small transporters' \
                .format(
                spyreport.metal if spyreport.metal != -1 else 'unknown',
                spyreport.crystal if spyreport.crystal != -1 else 'unknown',
                spyreport.deuterium if spyreport.deuterium != -1 else 'unknown',
                spyreport.cords,
                spyreport.planet,
                spyreport.fright_date,
                spyreport.defenseScore if spyreport.defenseScore != -1 else 'unknown',
                spyreport.resourcesTotal,
                spyreport.resourcesTotal * self.properties.PEROBES_LOOT,
                round(spyreport.resourcesTotal * self.properties.PEROBES_LOOT / self.properties.PROBES_SMALL_CARGOS, 2)
            )

            # format output
            if spyreport.defenseScore == 0:
                logger.info(message)
            elif spyreport.defenseScore == -1:
                logger.error(message)
            elif spyreport.defenseScore > 0:
                logger.warning(message)

        logger.info('Probs finished!')
        return spyreports

    ##################################
    # get best planets               #
    ##################################
    def get_best_planets(self):

        message = "Get all best planets"
        logger.info(message)
        self.telegram.send_message(message)

        all_inactive_planets = []

        for planet_cords in self.properties.PROBES_BEST_PLANETS:
            class Position:
                position = planet_cords

            all_inactive_planets.append(Position)

        return all_inactive_planets

    ##################################
    # run probes                     #
    ##################################
    def run_auto_probe(self, reports=[]):

        message = "Start with auto probe"
        logger.info(message)
        self.telegram.send_message(message)

        filtered_spy_reports = []

        while True:
            # get best spy reports
            if len(filtered_spy_reports) == 0:
                logger.info('In the filtered_spyreports list are NO planets left. Filter best planets'.format(
                    len(filtered_spy_reports)))

                if len(reports) == 0:
                    all_inactive_planets = self.get_best_planets()
                    self.send_probes(all_inactive_planets)
                    spy_reports = self.print_report(
                        int(len(all_inactive_planets) / 10) + (len(all_inactive_planets) % 10 > 0))  # print spy reports
                    return self.run_auto_probe(spy_reports)

                # get filter listed
                filtered_spy_reports = [report for report in reports if report.defenseScore == 0]
                # i = 0
                # while i <= 0:
                #    filtered_spy_reports.pop(0)
                #    i += 1
                filtered_spy_reports = [report for report in filtered_spy_reports if
                                        (report.resourcesTotal * self.properties.PEROBES_LOOT) >= self.properties.PROBES_SMALL_CARGOS * self.properties.PROBES_MIN_SMALL_CARGOS]
                filtered_spy_reports = filtered_spy_reports[:self.properties.PROBES_TAKE_PLANETS_LIMIT]
                report = []
            else:
                message = 'In the filtered_spyreports list are still {0} planets left'.format(len(filtered_spy_reports))
                logger.info(message)
                # self.telegram.send_message(message)

            # check filtered spy reports length
            if len(filtered_spy_reports) == 0:
                message = "Length of the filtered spy reports is null. Start to rescan best planets list"
                logger.info(message)
                return self.run_auto_probe()

            # wait for a free slot
            self.check_free_slots()

            # send cargos
            while self.properties.get_amount_probe_fleets() >= self.get_current_probes() and \
                    len(self.empire.friendly_fleet()) < self.properties.get_amount_max_fleets():
                if len(filtered_spy_reports) == 0:
                    message = "Length of the filtered spy reports is 0. Start to rescan best planets list"
                    logger.info(message)
                    self.telegram.send_message(message)
                    return self.run_auto_probe()

                target_planet = filtered_spy_reports[0]
                source_planet = None
                shortest_distance = None
                need_small_cargos = 0
                need_large_cargos = 0

                # send fleet
                for planet in self.empire.planet_ids():
                    # check if enough cargos is on planet
                    tmp_need_small_cargos = 0
                    tmp_need_large_cargos = 0

                    if self.empire.ships(planet).small_transporter.amount >= int(
                            math.ceil(target_planet.resourcesTotal * self.properties.PEROBES_LOOT / self.properties.PROBES_SMALL_CARGOS)):
                        tmp_need_small_cargos = int(
                            target_planet.resourcesTotal * self.properties.PEROBES_LOOT / self.properties.PROBES_SMALL_CARGOS)
                    elif self.empire.ships(planet).large_transporter.amount >= int(
                            math.ceil(target_planet.resourcesTotal * self.properties.PEROBES_LOOT / self.properties.PROBES_LARGE_CARGOS)):
                        tmp_need_large_cargos = int(
                            target_planet.resourcesTotal * self.properties.PEROBES_LOOT / self.properties.PROBES_LARGE_CARGOS)
                    else:
                        cargo_space = self.empire.ships(
                            planet).small_transporter.amount * self.properties.PROBES_SMALL_CARGOS + self.empire.ships(
                            planet).large_transporter.amount * self.properties.PROBES_SMALL_CARGOS
                        tmp_need_small_cargos = self.empire.ships(planet).small_transporter.amount
                        tmp_need_large_cargos = self.empire.ships(planet).large_transporter.amount
                        if int(math.ceil(target_planet.resourcesTotal * self.properties.PEROBES_LOOT)) > cargo_space:
                            logger.info(
                                'not enough cargos on the planet {0} available. check next planet with less resources'.format(
                                    planet))
                            continue

                    # get nearest planets
                    if shortest_distance == None:
                        shortest_distance = self.utils.distance(self.empire.celestial_coordinates(planet),
                                                                target_planet.cords)
                        source_planet = planet
                        need_small_cargos = tmp_need_small_cargos
                        need_large_cargos = tmp_need_large_cargos
                    else:
                        tmp_current_distance = self.utils.distance(self.empire.celestial_coordinates(planet),
                                                                   target_planet.cords)
                        if shortest_distance > tmp_current_distance and (
                                tmp_need_small_cargos > 0 or 0 < tmp_need_large_cargos):
                            shortest_distance = tmp_current_distance
                            source_planet = planet
                            need_small_cargos = tmp_need_small_cargos
                            need_large_cargos = tmp_need_large_cargos

                # send fleet
                response = False
                if need_large_cargos != 0 or need_small_cargos != 0:
                    try:
                        response = self.empire.send_fleet(mission.attack, source_planet,
                                                          self.utils.convertToCords(target_planet.cords),
                                                          [ships.large_transporter(need_large_cargos),
                                                           ships.small_transporter(need_small_cargos)])
                    except:
                        logger.error('Error during send fleets in run_auto_probe')
                        continue
                if response:
                    filtered_spy_reports.pop(0)
                    message = 'Send {0} large and {1} small cargos from {2} to {3}. In the filtered_spyreports list ' \
                              'are still {4} planets left'.format(
                        need_large_cargos,
                        need_small_cargos,
                        source_planet,
                        target_planet.cords,
                        len(filtered_spy_reports)
                    )
                    logger.info(message)
                    self.telegram.send_message(message)
                else:
                    filtered_spy_reports.pop(0)
                    logger.debug(
                        'No enough fleets on planet {0} available. Try next target with less resources'.format(
                            source_planet))
