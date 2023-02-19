from django.contrib import admin

from scorecard.models import Scorecard, ScoreLevel, ScoringItemLevel, ScoringItem
from scorecard.models import ScorecardVersion, ScoringItemVersion

admin.site.register(Scorecard)
admin.site.register(ScoreLevel)
admin.site.register(ScoringItemLevel)
admin.site.register(ScoringItem)

admin.site.register(ScorecardVersion)
admin.site.register(ScoringItemVersion)
