"""Django models for the scorch application.

All models for the app go in this file.
"""

from django.db import models

class EntityType(models.Model):
    """A type of Entity for which we want to create a Scorecard.

    These are usually the significant elements of the Enterprise
    Architecture.
    """
    name = models.CharField(max_length=50, unique=True,
        help_text='A type of entity for which a Scorecard will be'
            'created, such as Application.')
    description = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.name

class Entity(models.Model):
    """An instance of an object of a certain Entity Type.

    Entities are what are Scored in Scorecards.
    """
    name = models.CharField(max_length=250,
        help_text='The name of this entity.')
    description = models.TextField(max_length=1000,
        help_text='A description of the entity.')
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Entities'

    def __str__(self) -> str:
        return self.name

class Scorecard(models.Model):
    """Represents a Scorecard.

    Scorecards have ScorecardVersions, which track the structure.
    """
    name = models.CharField(max_length=100, unique=True,
        help_text='The name of the Scorecard, typically named for the'
            'Asset Type with which it is associated.')
    desciption = models.TextField(max_length=1000)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class ScorecardVersion(models.Model):
    """A version of a Scorecard.

    Versions track structure and can have Responses.
    """
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
    label = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'{self.scorecard} {self.label}'

class Response(models.Model):
    """A response to a Scorecard for an Entity."""
    scorecard_version = models.ForeignKey(ScorecardVersion,
        on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.scorecard_version} for {self.entity}'