from rest_framework import serializers
from teams.models import Match, Team
from users.models import Subscriber


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.StringRelatedField()
    kind = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ['country', 'id', 'kind', 'name']


class SubscriberSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)

    class Meta:
        model = Subscriber
        fields = ['type', 'method', 'teams', 'email', 'url']


class MatchSerializer(serializers.ModelSerializer):
    team_home = TeamSerializer()
    team_away = TeamSerializer()

    class Meta:
        model = Match
        fields = ['time', 'team_home', 'team_away', 'score_team_home', 'score_team_away', 'finished']
