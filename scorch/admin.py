from django.contrib import admin

from scorch.models import Attribute, AttributeValue
from scorch.models import EntityType, Entity, Task
from scorch.models import Scorecard, ScoreLevel, ScoringItemLevel, ScoringItem
from scorch.models import ScorecardVersion, ScoringItemVersion
from scorch.models import Response, ScoringItemResponse, Task

admin.site.register(Attribute)

admin.site.register(EntityType)
admin.site.register(Entity)
admin.site.register(AttributeValue)
admin.site.register(Task)

admin.site.register(Scorecard)
admin.site.register(ScoreLevel)
admin.site.register(ScoringItemLevel)
admin.site.register(ScoringItem)

admin.site.register(ScorecardVersion)
admin.site.register(ScoringItemVersion)

admin.site.register(Response)
admin.site.register(ScoringItemResponse)
