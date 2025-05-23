from django.contrib import admin

from applications.match.models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('local_team','local_team_score','away_team','away_team_score','date','status','referee','school_id','result')
