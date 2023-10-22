import factory
from factory.django import DjangoModelFactory

from vizcab import models


class Zone(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"zone {n}")
    surface = 40
    usage = models.Usage.HOUSING

    class Meta:
        model = models.Zone


class ConstructionProduct(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"product {n}")
    unite = "M2"
    production_impact = 17.5
    construction_impact = 2.1
    exploitation_impact = 0.6
    endoflife_impact = 0.3
    typical_lifetime = 50

    class Meta:
        model = models.ConstructionProduct


class ZoneProduct(DjangoModelFactory):
    zone = factory.SubFactory(Zone)
    product = factory.SubFactory(ConstructionProduct)
    quantity = 175.6

    class Meta:
        model = models.ZoneProduct


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


class ZoneWithTwoProducts(Zone):
    products_1 = factory.RelatedFactory(ZoneProduct, factory_related_name="zone")
    products_2 = factory.RelatedFactory(
        ZoneProduct,
        factory_related_name="zone",
        quantity=10,
        product__production_impact=56.0,
        product__construction_impact=74.0,
    )
    building = factory.SubFactory(Building)


class ZoneWithOneProduct(Zone):
    product = factory.RelatedFactory(
        ZoneProduct, factory_related_name="zone", quantity=5
    )
    building = factory.SubFactory(Building)
