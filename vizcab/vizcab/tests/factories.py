import factory
from factory.django import DjangoModelFactory

from vizcab import models


class Zone(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"zone {n}")
    surface = 40
    usage = models.Usage.HOUSING

    class Meta:
        model = models.Zone


class Building(DjangoModelFactory):
    class Meta:
        model = models.Building

    name = factory.Sequence(lambda n: f"building {n}")
    usage = models.Usage.HOUSING
    reference_period = 4


class BuildingWithTwoZones(Building):
    first_zone = factory.RelatedFactory(
        Zone, factory_related_name="building", surface=40
    )

    second_zone = factory.RelatedFactory(
        Zone, factory_related_name="building", surface=35.5
    )


class BuildingWithThreeZonesAndTwoUsage(Building):
    first_housing_zone = factory.RelatedFactory(
        Zone, factory_related_name="building", surface=40
    )

    second_housing_zone = factory.RelatedFactory(
        Zone, factory_related_name="building", surface=35.5
    )
    gymnasium_zone = factory.RelatedFactory(
        Zone,
        factory_related_name="building",
        surface=125.6,
        usage=models.Usage.GYMNASIUM,
    )
