from django.contrib import admin

from entity.models import Attribute, AttributeValue
from entity.models import EntityType, Entity

admin.site.register(Attribute)

admin.site.register(EntityType)
admin.site.register(Entity)
admin.site.register(AttributeValue)
