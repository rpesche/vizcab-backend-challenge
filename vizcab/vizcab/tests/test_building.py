from decimal import Decimal

from . import factories


class TestBuildingImpact:
    def test_nominal(self, db):
        building = factories.Building()
        factories.ZoneWithTwoProducts(building=building)
        factories.ZoneWithOneProduct(building=building)

        assert building.impact() == Decimal("5011.300")
