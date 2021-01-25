import time

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

                # check cache can be reduced

                    # gehe cache durch
                    # berechne differenz
                    # wenn die differenz kleiner gleich 0 ist -> löschen
                    # wenn die differenz größer 0 ist nichts machen: pass

                    #diff_minutes = self.utils.get_diff_minutes(self.empire.hostile_fleet()[0].arrival)
                    #print(diff_minutes)


                # checken ob attacke eine spio ist

                    # angreife loppen
                    # differenz von start und ankunft ausrechnen
                    # ist die differenz größer 10 minuten => Angriff => cache_liste speichern => Spio mit 11 probs verschicken vom angreifenden planeten
                    # Ansonsten ist es eine spio => telegram messagen => NICHT in cache speichern


                    # # save enemy to the cache
                    # if len(enemies_cache) == 0:
                    #     enemies_cache = self.empire.hostile_fleet()
                    # else:
                    #     tmp_enemies_cache = enemies_cache
                    #     enemies_cache = []
                    #     for new in self.empire.hostile_fleet():
                    #         exist = False
                    #         for old in tmp_enemies_cache:
                    #             if new.arrival == old.arrival:
                    #                 exist = True
                    #         if exist is False:
                    #             enemies_cache.append(new)


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


                # can entfernt werden
                # send message to enemy
                for current_enemy in enemies_cache:

                    #self.empire.send_message(current_enemy.player_id, 'Seid gegrüßt {0}! {1}'.format(
                    #                        current_enemy.player_name,
                    #                        random.choice(self.properties.SAVING_RANDOM_TEXT)
                    #                    ))

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
