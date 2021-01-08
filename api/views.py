from collections import OrderedDict

from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from teams.models import Match, Team
from users.models import Subscriber

from .serializers import MatchSerializer, SubscriberSerializer, TeamSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.select_related('country', 'kind').all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]


class SubsciberModelViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.select_related('user').prefetch_related('teams').all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def create(self, request):
        if request.data:
            data = request.data
            teams = Team.objects.filter(pk__in=data['teams'])

            try:
                obj = Subscriber.objects.create(user=request.user, type=data['type'], method=data['method'],
                                                url=data['url'], email=data['email'], token=data['token'])
                obj.teams.set(teams)
            except KeyError:
                return Response({'status': 400})

            return Response({'status': '201'})

        return Response({'status': 400})


class MatchModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def teams_user(self, user):
        return Subscriber.objects.filter(user__username=user).order_by('teams__name').distinct(
            'teams__name').values_list('teams__name', flat=True)

    def get_matches(self, teams):
        return self.queryset.filter(Q(team_home__name__in=teams) | Q(team_away__name__in=teams))

    def list(self, request):
        teams = self.teams_user(request.user)
        matches = self.get_matches(teams)
        return Response(MatchSerializer(matches, many=True).data)

    @action(detail=False, methods=['get'], name='Display last events')
    def last_events(self, request):
        teams = self.teams_user(request.user)
        matches = self.get_matches(teams)
        first = MatchSerializer(matches.filter(finished=False).order_by('-time').first()).data
        last = MatchSerializer(matches.order_by('-time').first()).data
        current = MatchSerializer(matches.filter(finished=False).filter(
            time__lte=timezone.now()).order_by('-time').first()).data
        context = OrderedDict([('subscribe_teams', teams), ('first_event', first),
                               ('last_event', last), ('current_event', current)])
        return Response(context)
