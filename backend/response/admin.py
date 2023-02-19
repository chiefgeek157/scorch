from django.contrib import admin

from response.models import Task
from response.models import Response, ScoringItemResponse

admin.site.register(Task)

admin.site.register(Response)
admin.site.register(ScoringItemResponse)
