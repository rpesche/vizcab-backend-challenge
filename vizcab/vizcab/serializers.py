from rest_framework.serializers import (
    ModelSerializer,
    DecimalField,
    CharField,
    Serializer,
)

from . import models


class Building(ModelSerializer):
    # TODO the `most_usage` is a usage in capital letter
    # We may make it as integer in the queryset and transform it to string in the serializers
    surface = DecimalField(max_digits=9, decimal_places=2)
    most_usage = CharField()

    class Meta:
        deep = 1
        model = models.Building
        fields = ["id", "name", "reference_period", "surface", "most_usage"]


class Impacts(Serializer):
    production_impacts = DecimalField(max_digits=9, decimal_places=2)
    construction_impacts = DecimalField(max_digits=9, decimal_places=2)
    endoflife_impacts = DecimalField(max_digits=9, decimal_places=2)
    exploitation_impact = DecimalField(max_digits=9, decimal_places=2)
