import time
import random

from ogame import OGame
from loguru import logger

class Saving(object):
    def __init__(self, properties, empire, telegram, utils):
        self.properties = properties
        self.empire: OGame = empire
        self.telegram = telegram
        self.utils = utils

    def auto_run_saving(self):

        enemies_cache = []

        while True:
            logger.info('Check if you get attacked or not')

            # check if you get attacked
            if self.empire.attacked():

                # save enemy to the cache
                if len(enemies_cache) == 0:
                    enemies_cache = self.empire.hostile_fleet()
                else:
                    tmp_enemies_cache = enemies_cache
                    enemies_cache = []
                    for new in self.empire.hostile_fleet():
                        exist = False
                        for old in tmp_enemies_cache:
                            if new.arrival == old.arrival:
                                exist = True
                        if exist is False:
                            enemies_cache.append(new)

                # save ressources
                # send spy probe

                # send message to enemy
                for current_enemy in enemies_cache:

                    #self.empire.send_message(current_enemy.player_id, 'Seid gegrüßt {0}! {1}'.format(
                                            current_enemy.player_name,
                                            random.choice(self.properties.SAVING_RANDOM_TEXT)
                                        ))

                    # report to me
                    message = '!!!!!!!! You are under attack from {0}, {2} at planet {3}. He arrives at {4} !!!!!!!!'.format(
                        current_enemy.player_name,
                        current_enemy.player_id,
                        current_enemy.origin,
                        current_enemy.destination,
                        current_enemy.arrival
                        )
                    logger.warning(message)
                    self.telegram.send_message(message)

                # update cache
                enemies_cache = self.empire.hostile_fleet()
            else:
                # reset list
                enemies_cache = []

            # wait xx seconds for next check
            time.sleep(self.properties.SAVING_RECHECK_ATTACKS)
