from django.urls import reverse
from django.test import Client
from rest_framework.status import HTTP_200_OK

from . import factories


class TestBuildingSurface:
    def test_building_with_no_zone(self, db):
        building = factories.Building()

        url = reverse("building-detail", args=(building.id,))
        response = Client().get(url)
        assert response.status_code == HTTP_200_OK
        assert response.json()["surface"] == "0.00"

    def test_building_with_two_zones(self, db):
        building = factories.BuildingWithTwoZones()

        url = reverse("building-detail", args=(building.id,))
        response = Client().get(url)
        assert response.status_code == HTTP_200_OK
        assert response.json()["surface"] == "75.50"


class TestBuildingMostUsage:
    def test_nominal(self, db):
        building = factories.BuildingWithThreeZonesAndTwoUsage()

        url = reverse("building-detail", args=(building.id,))
        response = Client().get(url)
        assert response.json()["most_usage"] == "GYMNASIUM"

    def test_housing_most_usage(self, db):
        building = factories.BuildingWithThreeZonesAndTwoUsage(
            second_housing_zone__surface=200.0
        )
        url = reverse("building-detail", args=(building.id,))

        response = Client().get(url)
        assert response.json()["most_usage"] == "HOUSING"

    def test_no_zone(self, db):
        building = factories.Building()
        url = reverse("building-detail", args=(building.id,))
        response = Client().get(url)
        assert response.json()["most_usage"] == ""
