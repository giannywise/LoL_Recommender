import requests
import pandas as pd
import time

"""
Datenvextraktions Struktur

Summoner Name --> summoner puuid --> matchhistory by puuid --> mathes by id --> grouped by champions
"""
key = open('key.txt').readlines()[0]

TIERS = ['MASTER', 'GRANDMASTER', 'CHALLENGER']


def get_sumnames():
    """
    rates for this request = 50 requests every 10 seconds
    """
    columns = ['summonerId', 'summonerName', 'leagueId']
    c = 0   # counter for requests
    df = pd.DataFrame()
    for t in TIERS:
        for p in range(1, 100):  # 100 requests every 2 minutes allowed p = page
            if p == 50:  # 50 request every 10 seconds allowed
                time.sleep(11)
            r = requests.get('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/'
                             'RANKED_SOLO_5x5/' + t + '/I?page=' + str(p) +
                             '&api_key=' + key)
            df2 = pd.DataFrame(r.json())
            if df2.empty == False and r.status_code == 200: # if request is not empty and successful
                print(t, r.status_code)
                try:    # if request is not empty
                    df = pd.concat([df[columns], df2[columns]], ignore_index=True)
                except KeyError:
                    df = pd.concat([df, df2[columns]], ignore_index=True)
            else:
                print('ERROR', t, r.status_code)
                df.to_json(f'summoner_names{c}.json')
        if df.shape[0] == 30000:    # if 30000 summoners are collected
            df.to_json(f'summoner_names{c}.json')
            c += 1
            print('CSV SAVED FINISHED')
            break
        else:
            df.to_json(f'summoner_names{c}.json')
            print('CSV SAVED')
            print('TIMER STARTED')
            time.sleep(121)
            print('TIMER ENDED')
    df.to_json(f'summoner_names{c}.json')
    print('CSV SAVED DONE')


def get_puuid():
    df = pd.read_json('summoner_names0.csv')
    df2 = pd.DataFrame()
    t = 0  # counter for requests
    for i in df['summonerId']:
        t += 1
        if t <= 100:
            r = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/'
                             + i + '?api_key=' + key)
            df3 = pd.DataFrame(r.json())
            print(r.status_code)
            df2 = pd.concat([df2, df3])
        else:
            t = 0
            print('TIMER STARTED')
            df2.to_csv('puuid{c}.csv')
            print('CSV SAVED')
            time.sleep(121)
            print('TIMER ENDED')

    df2.to_csv('puuid{c}.csv')
    print('CSV SAVED')


def get_matches_history():
    EXPORT_NAME = 'matchid.json'
    df = pd.read_json('puuid.json')
    df2 = pd.DataFrame()
    t = 0  # counter for requests
    j = 0  # counter for errors
    for i in df['puuid']:
        t += 1
        if t <= 100:
            r = requests.get(
                'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + i + '/ids?type=ranked&start=0&count=25&api_key=' + key)
            print('CODE:', r.status_code)
            if r.status_code == 200:
                df3 = pd.DataFrame([r.json()]).transpose()
                df2 = pd.concat([df2, df3], ignore_index=True)
            else:
                print('ERROR')
                j += 1
                df2.to_json(EXPORT_NAME)
                print(df2.shape[0], 'matches collected')
                print('JSON SAVED', j)
        else:
            t = 0
            df2.to_json(EXPORT_NAME)
            print('JSON SAVED', j)
            print(df2.shape[0], 'matches collected')
            print('TIMER STARTED')
            time.sleep(121)
            print('TIMER ENDED')
    print('JSON SAVED')


def get_unique_matches():
    df = pd.read_json('matchid.json').drop_duplicates()
    df.to_json('unique_matchid.json')


def get_match_info():
    df = pd.read_json('unique_matchid.json')
    df2 = pd.DataFrame()
    t = 0  # counter for 100 requests
    j = 0  # counter for errors
    c = 0  # counter for existing files
    EXPORT_NAME = f'matches{c}.json'
    rows = 0  # counter for rows each file extracted
    total_rows = 0  # counter for total rows extracted
    for i in df[0][total_rows:]:
        EXPORT_PRINT = 'JSON SAVED', 'ERRORS:', j, total_rows, 'matches collected', c + 1, ' files created', \
            'last created file:', EXPORT_NAME
        EXPORT_NAME = f'matches/matches{c}.json'
        total_rows += 1
        if rows < 5000:  # ~5000 rows each file
            t += 1
            if t <= 100:  # 100 requests every 2 minutes allowed
                r = requests.get('https://europe.api.riotgames.com/lol/match/v5/matches/' + i + '/?api_key=' + key)
                print('CODE:', r.status_code)
                if r.status_code == 200:    # if request is successful
                    df3 = pd.DataFrame([r.json()])
                    try:    # if there is no data in the file
                        df2 = pd.concat([df2['info'], df3['info']], ignore_index=True)
                    except KeyError:
                        df2 = pd.concat([df2, df3['info']], ignore_index=True)
                    rows += 1
                else:
                    print('ERROR ', r.status_code)
                    j += 1
                    df2.to_json(EXPORT_NAME)
                    print(EXPORT_PRINT)
            else:   # if 100 requests are made
                t = 0
                df2.to_json(EXPORT_NAME)
                print(EXPORT_PRINT)
                print('TIMER STARTED')
                time.sleep(121)
                print('TIMER ENDED')
        else:   # if 5000 rows are extracted
            rows = 0
            df2.to_json(EXPORT_NAME)
            print(EXPORT_PRINT)
            df2 = pd.DataFrame()
            c += 1
            print('DATAFRAME RESETTET', f'{c} Times')
            print('TIMER STARTED')
            time.sleep(121)
            print('TIMER ENDED')
    df2.to_json(EXPORT_NAME)
    print('FINAL JSON SAVED ', 'ERRORS:', j, total_rows, ' matches collected ', c + 1, ' files created')
