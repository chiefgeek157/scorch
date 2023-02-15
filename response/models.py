"""Models for the response application."""

from django.db import models

from entity.models import Entity
from scorecard.models import ScoreLevel, ScorecardVersion, ScoringItemVersion

class Task(models.Model):
    """A task to remediate a non-perfect score."""
    NOT_YET_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    TASK_STATUSES = [
        (NOT_YET_STARTED, 'Not Yet Started'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]

    HOURS = 1
    DAYS = 2
    WEEKS = 3
    MONTHS = 4
    UNITS = [
        (HOURS, 'hours'),
        (DAYS, 'days'),
        (WEEKS, 'weeks'),
        (MONTHS, 'months'),
    ]
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE,
        related_name='tasks')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=TASK_STATUSES)
    min_expense = models.FloatField(default=0.)
    max_expense = models.FloatField(default=0.)
    min_effort = models.FloatField(default=0.)
    max_effort = models.FloatField(default=0.)
    units = models.IntegerField(default=1, choices=UNITS)


class Response(models.Model):
    """A response to a Scorecard for an Entity."""
    DRAFT = 1
    COMPLETE = 2
    REVIEWED = 3
    STATUS = {
        (DRAFT, 'Draft'),
        (COMPLETE, 'Complete'),
        (REVIEWED, 'Reviewed'),
    }

    scorecard_version = models.ForeignKey(ScorecardVersion,
        on_delete=models.CASCADE, related_name='responses')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE,
        related_name='responses')
    status = models.IntegerField(choices=STATUS)
    scored_on = models.DateField(blank=True, null=True)
    scored_by = models.CharField(max_length=50, blank=True)
    reviewed_on = models.DateField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=50, blank=True)
    score = models.FloatField(editable=False, null=True)
    comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.scorecard_version} for {self.entity}'


class ScoringItemResponse(models.Model):
    """A response to a ScoringItem."""
    response = models.ForeignKey(Response, on_delete=models.CASCADE,
        related_name='scoring_item_responses')
    score_item_version = models.ForeignKey(ScoringItemVersion,
        on_delete=models.CASCADE, related_name='scoring_item_responses')
    score_level = models.ForeignKey(ScoreLevel, blank=True, null=True,
        on_delete=models.CASCADE, related_name='scoring_item_responses')
    weight = models.FloatField(blank=True, null=True)
    mandatory = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True)
    score = models.FloatField(editable=False, null=True)
    tasks = models.ManyToManyField(Task, related_name='scoring_item_responses')

    def __str__(self) -> str:
        return f'{self.score_item_version.score_item.text}: {self.score_level}'
