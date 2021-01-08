from django.contrib import admin

from .models import Country, Kind, Match, Team


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind_name')
    search_fields = ('name',)

    def kind_name(self, obj):
        return obj.kind.name
    kind_name.short_description = 'Rodzaj'
    kind_name.allow_tags = True


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('time', 'team_home_name', 'team_away_name', 'archive', 'continues')

    def team_home_name(self, obj):
        return obj.team_home.name
    team_home_name.short_description = 'U siebie'
    team_home_name.allow_tags = False

    def team_away_name(self, obj):
        return obj.team_away.name
    team_away_name.short_description = 'Na wyjeździe'
    team_away_name.allow_tags = False
