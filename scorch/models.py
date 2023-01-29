"""Django models for the scorch application.

All models for the app go in this file.
"""

from django.db import models
from django.db.models import F, Q


class Attribute(models.Model):
    """An attribute deinfes a property Entities may have.

    Attributes can be shared across EntityTypes.
    """
    TEXT = 1
    STRING = 2
    FLOAT = 3
    INTEGER = 4
    BOOLEAN = 5
    DATE = 6
    TYPES = [
        (TEXT, 'Text'),
        (STRING, 'String'),
        (FLOAT, 'Float'),
        (INTEGER, 'Integer'),
        (BOOLEAN, 'Boolean'),
        (DATE, 'Date'),
    ]

    name = models.CharField(max_length=50, unique=True)
    type = models.IntegerField(choices=TYPES)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class EntityType(models.Model):
    """A type of Entity for which we want to create a Scorecard.

    These are usually the significant elements of the Enterprise
    Architecture.
    """
    name = models.CharField(max_length=50, unique=True,
        help_text='A type of entity for which a Scorecard will be'
            'created, such as Application.')
    description = models.TextField(blank=True)
    attributes = models.ManyToManyField(Attribute, related_name='entity_types')

    def __str__(self) -> str:
        return self.name


class Entity(models.Model):
    """An instance of an object of a certain Entity Type.

    Entities are what are Scored in Scorecards.
    """
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE,
        related_name='entities')
    name = models.CharField(max_length=250,
        help_text='The name of this entity.')
    description = models.TextField(blank=True,
        help_text='A description of the entity.')

    class Meta:
        verbose_name_plural = 'Entities'

    def __str__(self) -> str:
        return self.name


class AttributeValue(models.Model):
    """The value of an Attribute for an Entity."""
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE,
        related_name='attribute_values')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
        related_name='values')
    value_str = models.TextField(blank=True, null=True)
    value_int = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_bool = models.BooleanField(blank=True, null=True)
    value_date = models.DateField(blank=True, null=True)

    def value(self) -> tuple[int, any]:
        val = None
        match self.attribute.type:
            case Attribute.STRING:
                val = self.value_str
            case Attribute.INTEGER:
                val = self.value_int
            case Attribute.FLOAT:
                val = self.value_float
            case Attribute.BOOLEAN:
                val = self.value_bool
            case Attribute.DATE:
                val = self.value_date
        return (self.attribute.type, val)

    def __str__(self) -> str:
        return f'{self.entity}: {self.attribute.type}[{self.value()}]'


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
