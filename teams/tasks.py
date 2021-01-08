import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.template import Context, Template
from django.utils import timezone
from teams.models import Kind, Match, Team
from teams.utils import endpoint, get_events

EMAIL = '''
<!DOCTYPE html>
<html lang="pl" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>
    <body>
        <p>Otrzymujesz wiadomość ponieważ drużyna, którą sybskrybujesz bierze udział w&nbsp;wydarzeniu:</p>
        <p>{{team_home}} - {{team_away}}<p>
        <p>Z poważniem<br/>Zespół Scores</p>
    </body>
</html>
'''

EMAIL_LIVE = '''
    <!DOCTYPE html>
    <html lang="pl" dir="ltr">
        <head>
            <meta charset="utf-8">
            <title></title>
        </head>
        <body>
            <p>Otrzymujesz wiadomość ponieważ drużyna, którą sybskrybujesz bierze udział w&nbsp;wydarzeniu:</p>
            <p>{{team_home}} - {{team_away}}<p>
            <p>Nowy wynik w spotkaniu: {{score_home}} - {{score_away}}</p>
            <p>Z poważniem<br/>Zespół Scores</p>
        </body>
    </html>
'''


def get_time(type_):
    if type_ == 'live':
        time = timezone.now() - datetime.timedelta(seconds=10 * 60)
    elif type_ == 'week':
        time = timezone.now() - datetime.timedelta(days=7)
    else:
        time = timezone.now().date()

    return time


@shared_task
def update_scores():
    types = Kind.objects.values_list('name', flat=True)

    for type_, time, home, away in get_events(types):
        try:
            kind = Kind.objects.get(name=type_[1])
        except Kind.DoesNotExist as exc:
            print(exc, type_)

            continue
        home_obj, h_create = Team.objects.get_or_create(name=home[0], defaults={'kind': kind})
        away_obj, a_create = Team.objects.get_or_create(name=away[0], defaults={'kind': kind})
        match_obj, m_created = Match.objects.get_or_create(team_home=home_obj, team_away=away_obj,
                                                           defaults={'time': time[1], 'score_team_home': home[1],
                                                                     'score_team_away': away[1], 'continues': True})

        if not m_created:
            match_obj.score_team_home = home[1]
            match_obj.score_team_away = away[1]
            match_obj.save()


@shared_task
def send_email(type_):
    time = get_time(type_)

    matches = Match.objects.filter(time__gte=time)
    emails = []

    for match in matches:
        qs1 = match.team_home.subscribes.filter(email__isnull=False, type=type_)
        qs2 = match.team_away.subscribes.filter(email__isnull=False, type=type_)
        emails.extend(list(qs2.union(qs1).values_list('email', flat=True)))

        if type_ == 'live':
            tmpl = Template(EMAIL_LIVE)
            context = Context({'team_home': match.team_home.name, 'team_away': match.team_away.name,
                               'score_home': match.score_team_home, 'score_away': match.score_team_away})
        else:
            tmpl = Template(EMAIL)
            context = Context({'team_home': match.team_home.name, 'team_away': match.team_away.name})

        content = tmpl.render(context)
        emails.append(('Wydarzenie sportowe', content, settings.NO_REPLY_ADRES_EMAIL, emails))

    send_mass_mail(tuple(emails))


@shared_task
def post_to_endpoint(type_):
    time = get_time(type_)

    matches = Match.objects.filter(Q(team_home__name='FC Barcelona') | Q(team_away__name='FC Barcelona'),
                                   time__gte=time, continues=True)
    events = []

    for match in matches:
        qs1 = match.team_home.subscribes.filter(url__isnull=False, type=type_)
        qs2 = match.team_away.subscribes.filter(url__isnull=False, type=type_)

        if type_ == 'live':
            context = {'TA': match.team_away.name,
                       'TH': match.team_away.name,
                       'SA': match.score_team_away,
                       'SH': match.score_team_home}
        else:
            context = {'TA': match.team_away.name,
                       'TH': match.team_away.name,
                       'SE': match.time}

        events.extend({
            'urls': list(qs2.union(qs1).values_list('url', flat=True)),
            'context': context})

    for event in events:
        context = event['conext']

        for url in event['urls']:
            endpoint(url, context)
