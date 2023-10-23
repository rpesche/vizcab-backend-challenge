from decimal import Decimal

from django.urls import reverse
from django.test import Client
from rest_framework.status import HTTP_200_OK

from . import factories


class TestBuildingImpact:
    def test_nominal(self, db):
        building = factories.Building()
        factories.ZoneWithTwoProducts(building=building)
        factories.ZoneWithOneProduct(building=building)

        assert building.impact() == Decimal("5011.300")


class TestImpactsEndpoint:
    def test_get_impacts(self, db):
        building = factories.Building()
        factories.ZoneWithTwoProducts(building=building)
        factories.ZoneWithOneProduct(building=building)

        url = reverse("building-impacts", args=(building.id,))
        response = Client().get(url)
        assert response.status_code == HTTP_200_OK
        assert response.json() == {
            "production_impacts": 3720.5,
            "construction_impacts": 1119.26,
            "endoflife_impacts": 57.18,
            "exploitation_impact": 114.36,
        }
