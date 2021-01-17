class Properties(object):
    ########################
    # bots                 #
    ########################
    BOT_PROBE = False
    BOT_SAVE = True
    BOT_EXPEDITIONS = True

    ########################
    # Properties 4 probes  #
    ########################
    PROBES_RECHECK = 45

    PROBES_BEST_PLANETS = [
        [1, 29, 8, 1],
        [1, 33, 7, 1],
        [1, 34, 11, 1],
        [1, 54, 9, 1],
        [1, 71, 12, 1],
        [1, 79, 3, 1],
        [1, 83, 3, 1],
        [1, 83, 7, 1],
        [1, 83, 10, 1],
        [1, 91, 5, 1],
        [1, 91, 8, 1],
        [1, 94, 9, 1],
        [1, 114, 4, 1],
        [1, 114, 7, 1],
        [1, 115, 12, 1],
        [1, 121, 7, 1],
        [1, 154, 3, 1],
        [1, 154, 11, 1],
        [1, 277, 8, 1],
        [1, 392, 6, 1],
        [1, 423, 6, 1],
        [1, 441, 4, 1],
        [1, 467, 8, 1],
        [1, 467, 6, 1],
        [1, 480, 7, 1],

        [2, 28, 5, 1],
        [2, 28, 7, 1],
        [2, 28, 12, 1],
        [2, 30, 6, 1],
        [2, 33, 7, 1],
        [2, 33, 8, 1],
        [2, 33, 11, 1],
        [2, 52, 8, 1],
        [2, 160, 12, 1],
        [2, 168, 4, 1],
        [2, 169, 4, 1],
        [2, 169, 5, 1],
        [2, 169, 6, 1],
        [2, 172, 8, 1],
        [2, 173, 4, 1],
        [2, 173, 8, 1],
        [2, 173, 9, 1],
        [2, 175, 12, 1],
        [2, 181, 8, 1],
        [2, 210, 9, 1],
        [2, 211, 7, 1],
        [2, 213, 7, 1],
        [2, 218, 9, 1],
        [2, 218, 10, 1],
        [2, 220, 9, 1],
        [2, 230, 7, 1],
        # [2, 234, 6, 1], urlaubsmodous
        [2, 235, 7, 1],
        [2, 247, 6, 1],
        [2, 253, 10, 1],
        [2, 250, 7, 1],
        [2, 254, 6, 1],
        [2, 254, 7, 1],
        [2, 254, 12, 1],
        # [2, 255, 6, 1], noob protection
        # [2, 255, 9, 1], noob protection
        [2, 255, 11, 1],
        [2, 256, 4, 1],
        [2, 256, 9, 1],
        [2, 257, 11, 1],
        [2, 262, 8, 1],
        [2, 262, 10, 1],
        [2, 271, 7, 1],
        [2, 275, 6, 1],
        [2, 288, 8, 1],
        [2, 288, 11, 1],
        [2, 288, 12, 1],
        [2, 299, 9, 1],
        [2, 316, 8, 1],
        [2, 333, 7, 1],
        [2, 333, 9, 1],
        [2, 333, 10, 1],
        [2, 345, 5, 1],
        [2, 245, 5, 1],
        [2, 345, 6, 1],
        [2, 346, 7, 1],
        [2, 351, 4, 1],
        [2, 351, 6, 1],
        [2, 351, 10, 1],
        [2, 356, 8, 1],
        [2, 359, 7, 1],
        [2, 385, 7, 1],
        [2, 385, 8, 1],
        [2, 387, 11, 1],
        [2, 388, 5, 1],
        [2, 388, 7, 1],
        [2, 390, 6, 1],
        [2, 414, 6, 1],
        [2, 420, 12, 1],
        [2, 438, 12, 1],
        [2, 436, 4, 1],
        [2, 441, 6, 1],
        [2, 441, 12, 1],
        [2, 454, 12, 1],
        [2, 454, 4, 1],
        [2, 456, 9, 1],
        [2, 459, 6, 1],
        [2, 479, 8, 1],
        [2, 480, 4, 1],
        [2, 487, 11, 1],
        [2, 494, 8, 1],

        [3, 117, 4, 1],
        # [3, 126, 12, 1],
        [3, 132, 7, 1],
        [3, 139, 6, 1],
        [3, 141, 8, 1],
        [3, 144, 1, 1],
        [3, 144, 13, 1],
        [3, 144, 14, 1],
        [3, 151, 12, 1],
        [3, 152, 5, 1],
        [3, 170, 6, 1],
        [3, 172, 4, 1],
        [3, 173, 8, 1],
        [3, 186, 5, 1],
        [3, 186, 6, 1],
        [3, 186, 7, 1],
        [3, 205, 6, 1],
        [3, 222, 10, 1],
    ]

    PROBES_BLACKLIST = [
        [2, 95, 4, 1],
        [2, 149, 11, 1],
        [2, 430, 7, 1]
    ]

    PROBES_AMOUNT_OF_SONDES = 11

    PEROBES_LOOT = 0.75 #75 percent
    PROBES_MIN_SMALL_CARGOS = 30

    PROBES_SMALL_CARGOS = 7000
    PROBES_LARGE_CARGOS = 35000

    # if true, all inactive planets will be scanned
    PROBES_DELETE_OLD_SPY_REPORTS = True
    PROBES_TAKE_BEST_PLANETS = True
    PROBES_TAKE_PLANETS_LIMIT = 25

    PROBES_TAKE_OLD_SPY_REPORTS = False
    if PROBES_TAKE_OLD_SPY_REPORTS:
        PROBES_DELETE_OLD_SPY_REPORTS = False
    PROBES_LENGTH_OLD_SPY_REPORTS = 10

    PROBES_GALAXY_RANGE = [2, 2]  # [1, 6]
    PROBES_SYSTEM_RANGE = [1, 499]  # [1, 499]

    #################################
    # Properties 4 saving           #
    #################################
    SAVING_RECHECK_ATTACKS = 180

    SAVING_RANDOM_TEXT = [
        '“Houston, we’ve had a problem.” - Jim Lovell, Kommandant von Apollo 13, aus rund 300.000 km Entfernung von der Erde. Ihm konnte zum Glück geholfen werden, aber wie kann ich denn euch weiterhelfen?',
        'Ein Witz aus meiner Witzkiste: "Sagt ein Mann zu seinem Freund: „Meine Frau macht eine dreiwöchige Diät.“ „Und wie viel hat sie schon verloren?“ „Zwei Wochen.“" Aber mich stellt sich nun die Frage wie ich euch helfen kann?',
        'Ist bei euch das Wetter auch so herrlich wie bei mir? Wie kann ich denn weiterhelfen?',
        'Darf ich dir ein Geheimnis erzählen? Ich habe einen Joghurt fallen gelassen. Er war nicht mehr haltbar. Wie kann ich euch weiterhelfen?',
        'Ist denn schon Weihnachten? Wie kann ich euch helfen?'
    ]

    #################################
    # Properties 4 expeditions      #
    #################################
    EXPEDITIONS_RECHECK = 120
    EXPEDITIONS_DURATION = 1
    EXPEDITIONS_ONLY_LARGE_CARGOS = True
    EXPEDITIONS_LARGE_CARGOS = 100
    EXPEDITIONS_SMALL_CARGOS = 200

    EXPEDITIONS_RANGE = 0


    def __init__(self, empire):
        self.empire = empire
        self = self

    def get_source_planet(self):
        planetMILLET = self.empire.planet_ids()[0]  # galaxy 3:162:4
        planetORTOVOX = self.empire.planet_ids()[1]  # galaxy 1:97:12
        planetMAMMUT = self.empire.planet_ids()[2]  # galaxy 2:93:12
        planetARCTARYX = self.empire.planet_ids()[3]  # galaxy 2:299:10
        planetPETZL = self.empire.planet_ids()[4]  # galaxy 1:300:6
        return planetMAMMUT

    # calculate the maximal amount of fleets
    def get_amount_max_fleets(self):
        # default fleet is + 1; change if you have an other default value
        # + 0 because one slot will be always free for an emergency
        maxFleets = self.empire.research().computer.level + 0
        return maxFleets

    # calc amount for expedtions
    def get_amount_expeditions_fleets(self):
        level = self.empire.research().astrophysics.level
        bonus = 3
        fleets = 0 + bonus

        if level >= 25:
            fleets += 4
        elif level >= 16:
            fleets += 3
        elif level >= 9:
            fleets += 2
        elif level >= 4:
            fleets += 1
        elif level >= 1:
            fleets += 0

        return fleets

    # calc amount for spy robes
    def get_amount_probe_fleets(self):
        if self.BOT_EXPEDITIONS:
            return self.get_amount_max_fleets() - self.get_amount_expeditions_fleets()
        else:
            return self.get_amount_max_fleets()