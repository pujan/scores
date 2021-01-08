import datetime

import requests
import json

from django.core.mail import send_mass_mail


def data_from_22bet():
    url = 'https://22bet9.info/LiveFeed/GetTopGamesStatZip?lng=pl&partner=151'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://22bet9.info/pl/?tag=d_460479m_7669c_'
    }

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return {'Success': False}

    return resp.json()


def get_events(types):
    data = data_from_22bet()

    if not data['Success']:
        return

    for event in data['Value']:
        if event['SN'] in types:
            try:
                team_home = event['O1E']
                team_away = event['O2E']
                scores_team_home = event['SC']['FS']['S1']
                scores_team_away = event['SC']['FS']['S2']
                time = datetime.datetime.fromtimestamp(event['S'])
            except KeyError:
                continue

            yield (('type', event['SN']), ('time', time), (team_home, scores_team_home), (team_away, scores_team_away))


def endpoint(url, context):
    if isinstance(context, dict):
        context = json.dumps(context)

    auth = ('lukasz', 'ToHaselkoJest0K')
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json; indent=4'}
    return requests.post(url, auth=auth, data=context, headers=headers)
