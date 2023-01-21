"""Django models for the scorch application.

All models for the app go in this file.
"""

from django.db import models

class Scorecard(models.Model):
    """Represents a Scorecard.

    Scorecards have ScorecardVersions, which track the structure.
    """
    name = models.CharField(max_length=100)
    desciption = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.name

class ScorecardVersion(models.Model):
    """A version of a Scorecard.

    Versions track structure and can have Responses.
    """
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
    label = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.label
