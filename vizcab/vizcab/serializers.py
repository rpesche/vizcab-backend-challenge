from rest_framework.serializers import ModelSerializer, DecimalField, CharField

from . import models


class Building(ModelSerializer):
    # TODO the `most_usage` is a usage in capital letter
    # We may make it as integer in the queryset and transform it to string in the serializers
    surface = DecimalField(max_digits=9, decimal_places=2)
    most_usage = CharField()

    class Meta:
        deep = 1
        model = models.Building
        fields = ["id", "name", "usage", "reference_period", "surface", "most_usage"]
