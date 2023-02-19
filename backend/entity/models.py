from django.db import models


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