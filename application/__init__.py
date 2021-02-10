#!/usr/bin/python

import configparser
import os
import threading
import logging

from debrisField import DebrisField
from saving import Saving
from expedition import Expedition
from utils import Utils
from properties import Properties
from probe import Probe
from loguru import logger

########################
# run prob bot         #
########################
def run_prob_bot(test_):
    logging.info("Thread %s: starting", 'run_prob_bot')

    probe = Probe(properties, empire, telegram, utils)
    all_inactive_planets = []
    if properties.PROBES_TAKE_BEST_PLANETS and properties.PROBES_DELETE_OLD_SPY_REPORTS is True:
        all_inactive_planets = probe.get_best_planets()
    elif properties.PROBES_TAKE_BEST_PLANETS is False and properties.PROBES_DELETE_OLD_SPY_REPORTS is True:
        all_inactive_planets = probe.get_inactive_planetsself()  # get inactives planets

    # send probes
    spy_reports = None
    if properties.PROBES_DELETE_OLD_SPY_REPORTS is False:
        spy_reports = probe.print_report(properties.PROBES_LENGTH_OLD_SPY_REPORTS)
    else:
        probe.send_probes(all_inactive_planets)
        spy_reports = probe.print_report(
            int(len(all_inactive_planets) / 10) + (len(all_inactive_planets) % 10 > 0))  # print spy reports
    probe.run_auto_probe(spy_reports)

    logging.info("Thread %s: finishing", 'run_prob_bot')

########################
# run debris bot       #
########################
def run_debris_bot(test_):
    logging.info("Thread %s: starting", 'run_debris_bot')

    debris = DebrisField(properties, empire, telegram, utils)
    debris.auto_collect_debris_fields()

    logging.info("Thread %s: finishing", 'run_debris_bot')

########################
# run save bot         #
########################
def run_save_bot(test_):
    logging.info("Thread %s: starting", 'run_save_bot')

    saving = Saving(properties, empire, telegram, utils)
    saving.auto_run_saving()

    logging.info("Thread %s: finishing", 'run_save_bot')

########################
# run expedition bot   #
########################
def run_expedition_bot(test_):

    logging.info("Thread %s: starting", 'run_expedition_bot')

    expedition = Expedition(properties, empire, telegram, utils)
    expedition.auto_run_expedition()

    logging.info("Thread %s: finishing", 'run_expedition_bot')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # init log
    logger.add("log/file_{time}.log")

    # vars
    config = configparser.ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, '../config.cfg'))

    # init objects
    utils = Utils(config['Login'], config['Telegram'])
    empire = utils.empire
    telegram = utils.telegram
    properties = Properties(empire)

    try:
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

        threads = list()

        # thread probes
        if properties.BOT_PROBE:
            logging.info("Main    : create and start thread %s.", 'probs')
            bot_prob = threading.Thread(target=run_prob_bot, args=(properties,))
            threads.append(bot_prob)
            bot_prob.start()

        # thread saving
        if properties.BOT_EXPEDITIONS:
            logging.info("Main    : create and start thread %s.", 'expeditions')
            bot_expedition = threading.Thread(target=run_expedition_bot, args=(properties,))
            threads.append(bot_expedition)
            bot_expedition.start()

        # thread saving
        if properties.BOT_SAVE:
            logging.info("Main    : create and start thread %s.", 'saving')
            bot_saving = threading.Thread(target=run_save_bot, args=(properties,))
            threads.append(bot_saving)
            bot_saving.start()

        # thread debris
        if properties.BOT_DEBRIS:
            logging.info("Main    : create and start thread %s.", 'debris')
            bot_debris = threading.Thread(target=run_debris_bot, args=(properties,))
            threads.append(bot_debris)
            bot_debris.start()

        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)
    except:
        print("Error: unable to start thread")

    while 1:
        pass


