"""Django models for the scorecard application."""

from django.db import models

from entity.models import EntityType


class Scorecard(models.Model):
    """Represents a Scorecard.

    Scorecards have ScorecardVersions, which track the structure.
    """
    DEFAULT_MAX_SCORE = 100.0
    DEFAULT_SCORE_LEVEL_LABEL = 'Conformance'
    DEFAULT_WEIGHT = 100.0
    DEFAULT_MANDATORY = False

    WEIGHTED_DEDUCTION_SCORER = 1
    SCORER_TYPES = [
        (WEIGHTED_DEDUCTION_SCORER, 'Weighted Deduction Scorer')
    ]
    DEFAULT_SCORER_TYPE = WEIGHTED_DEDUCTION_SCORER

    THRESHHOLD_SCORE_LEVEL_COMPUTER = 1
    SCORE_LEVEL_COMPUTER_TYPES = [
        (THRESHHOLD_SCORE_LEVEL_COMPUTER, 'Threshhold Score Level Computer')
    ]
    DEFAULT_SCORE_LEVEL_COMPUTER = THRESHHOLD_SCORE_LEVEL_COMPUTER

    EXPRESSION_WEIGHT_COMPUTER = 1
    WEIGHT_COMPUTER_TYPES = [
        (EXPRESSION_WEIGHT_COMPUTER, 'Expression Weight Computer')
    ]
    DEFAULT_WEIGHT_COMPUTER = EXPRESSION_WEIGHT_COMPUTER

    EXPRESSION_MANDATORY_COMPUTER = 1
    MANDATORY_COMPUTER_TYPES = [
        (EXPRESSION_MANDATORY_COMPUTER, 'Expression Mandatory Computer')
    ]
    DEFAULT_MANDATORY_COMPUTER = EXPRESSION_MANDATORY_COMPUTER

    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE,
        related_name='scorecards')
    name = models.CharField(max_length=100, unique=True,
        help_text='The name of the Scorecard, typically named for the'
            'Asset Type with which it is associated.')
    desciption = models.TextField(blank=True)
    max_score = models.FloatField(default=DEFAULT_MAX_SCORE,
        help_text='The maximum score allowed for any item.')
    score_level_label = models.CharField(max_length=50,
        default=DEFAULT_SCORE_LEVEL_LABEL)
    default_weight = models.FloatField(default=DEFAULT_WEIGHT,
        help_text='The default weight applied'
        'to all ScoreItems if they do not have an override or formula.')
    default_mandatory = models.BooleanField(default=DEFAULT_MANDATORY)
    scorer_type = models.IntegerField(choices=SCORER_TYPES,
        default=DEFAULT_SCORER_TYPE)
    score_level_computer_type = models.IntegerField(
        choices=SCORE_LEVEL_COMPUTER_TYPES,
        default=DEFAULT_SCORE_LEVEL_COMPUTER)
    weight_computer_type = models.IntegerField(
        choices=WEIGHT_COMPUTER_TYPES, default=DEFAULT_WEIGHT_COMPUTER)
    mandatory_computer_type = models.IntegerField(
        choices=MANDATORY_COMPUTER_TYPES, default=DEFAULT_MANDATORY_COMPUTER)

    def __str__(self) -> str:
        return self.name


class ScoreLevel(models.Model):
    """A level to choose when directly scoring or compute."""
    scorecard = models.ForeignKey(Scorecard, related_name='score_levels',
        on_delete=models.CASCADE)
    order = models.PositiveIntegerField(help_text='The order of this '
        'ScoreLevel among its peers within the scorecard.')
    name = models.CharField(max_length=20)
    score = models.FloatField(help_text='The score assigned by this'
        'level when directly chosen, must be <= the Scorecard max score.')
    threshold = models.FloatField(help_text='The lower value at which this '
        'level is displayed for computed scores. Must be less than score '
        'to be useful.')

    def __str__(self) -> str:
        return f'{self.name}'


class ScoringItemLevel(models.Model):
    """A level of ScoringItems.

    Levels represent the structure of a Scorecard. ScoringItems at
    the top level have no parents, and at the bottom have no
    children.
    """
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE,
        related_name='score_item_levels')
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(help_text='The order of the '
        'ScoringItemLevel among its peers within the Scorecard.')
    help_base_url = models.URLField(help_text='The base URL for autogenerated'
        'links to further help ScoreItems at this level')

    def is_first(self) -> bool:
        """Return True if this level is the first."""
        return (self.order == 1)

    def is_last(self) -> bool:
        """Return True if this level is the last."""
        return (self.order == len(self.scorecard.score_item_levels))

    def __str__(self) -> str:
        return self.name


class ScoringItem(models.Model):
    """A statement to be scored.

    Only the structure of a ScoringItem is versioned.
    """
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE,
        related_name='scoring_items')
    level = models.ForeignKey(ScoringItemLevel, on_delete=models.CASCADE,
        related_name='scoring_items')
    text = models.TextField()
    explanation = models.TextField(blank=True)
    owner = models.CharField(max_length=50, blank=True, null=True)
    weight_expr = models.TextField(blank=True, null=True)
    mandatory_expr = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.text


class ScorecardVersion(models.Model):
    """A version of a Scorecard.

    Versions track structure and can have Responses. A ScorecardVersion
    has a list of child ScoringItemVersions that are the top level
    of the ScoringItem tree.
    """
    scorecard = models.ForeignKey(Scorecard, on_delete=models.CASCADE,
        related_name='versions')
    label = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'{self.scorecard} {self.label}'


class ScoringItemVersion(models.Model):
    """Contains version-speicifc structure.

    ScoreItemVersion all belong to the same ScorecardVersion for
    simplicity. When a Scorecard is reved, all ScoreItems are also
    reved. This keep tree navigation simple as it is a true tree
    and not a DAG.

    Only ScoreItemVersion at ScoreItemLevel.order = 1 have the
    scorecare_version set, which also means parent will not be set.

    ScoreItemVersions at the bottom will have no children.

    Changes to owner, weight, or mandatory cause a revision.
    """
    scorecard_version = models.ForeignKey(ScorecardVersion,
        related_name='scoring_item_versions', on_delete=models.CASCADE)
    scoring_item = models.ForeignKey(ScoringItem, related_name='versions',
        on_delete=models.CASCADE)
    parent = models.ForeignKey('ScoringItemVersion', blank=True, null=True,
        on_delete=models.CASCADE, related_name='children')

    def __str__(self) -> str:
        return f'{self.score_item.text} {self.get_label()}'
