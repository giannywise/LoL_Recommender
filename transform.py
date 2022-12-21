import pandas as pd
import os

"""
Data transformation structure

"""

info = ['gameDuration', 'participants']  # first nested dict
participants = ['championName', 'damageDealtToTurrets', 'damageDealtToObjectives', 'damageDealtToChampions',
                'damageDealtToBuildings', 'damageSelfMitigated', 'deaths', 'detectionWardsBoughtInGame',
                'detectorWardsPlaced', 'doubleKills', 'firstBloodAssist', 'firstBloodKill', 'firstTowerAssist',
                'firstTowerKill', 'individualPosition', 'inhibitorKills', 'inhibitorTakedowns', 'kills',
                'killingsprees', 'largestMultiKill', 'longestTimeSpentLiving', 'magicDamageDealt',
                'magicDamageDealtToChampions', 'magicDamageTaken', 'neutralMinionsKilled',
                'neutralMinionsKilledEnemyJungle', 'neutralMinionsKilledTeamJungle', 'pentaKills',
                'physicalDamageDealt', 'physicalDamageDealtToChampions', 'physicalDamageTaken', 'quadraKills',
                'sightWardsBoughtInGame', 'teamPosition', 'timeCCingOthers', 'totalDamageDealt',
                'totalDamageDealtToChampions', 'totalDamageShieldedOnTeammates', 'totalDamageTaken', 'totalHeal',
                'totalMinionsKilled', 'totalTimeCrowdControlDealt', 'totalTimeSpentDead', 'tripleKills',
                'trueDamageDealt', 'trueDamageDealtToChampions', 'trueDamageTaken', 'turretKills', 'turretTakedowns',
                'visionScore', 'visionWardsBoughtInGame', 'wardsKilled']  # second nested dict

