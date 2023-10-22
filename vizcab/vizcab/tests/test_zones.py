from decimal import Decimal

from . import factories


class TestZoneImpact:
    def test_impact_production(self, db):
        zone = factories.ZoneWithTwoProducts()
        production_impact, _, _ = zone.impacts()
        production_impact == Decimal("3633")

    def test_impact_construction(self, db):
        zone = factories.ZoneWithTwoProducts()
        _, construction_impact, _ = zone.impacts()
        assert construction_impact == Decimal("1108.76")

    def test_impact_endoflife(self, db):
        zone = factories.ZoneWithTwoProducts()

        _, _, endoflife_impact = zone.impacts()
        assert endoflife_impact == Decimal("55.68")
