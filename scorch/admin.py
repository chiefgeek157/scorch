from django.contrib import admin

from .models import EntityType, Entity, Scorecard, ScorecardVersion, Response

admin.site.register(EntityType)
admin.site.register(Entity)
admin.site.register(Scorecard)
admin.site.register(ScorecardVersion)
admin.site.register(Response)
