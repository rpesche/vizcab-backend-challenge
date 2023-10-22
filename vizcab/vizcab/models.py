from decimal import Decimal

from django.db import models


UNITES = [
    ("KG", "Kilogram"),
    ("M", "Meter"),
    ("M2", "Square meter"),
    ("mL", "Linear meter"),
]


class Usage(models.IntegerChoices):
    HOUSING = 1, "Logement collectif"
    OFFICES = 2, "Bureaux"
    GYMNASIUM = 3, "Etablissement sportif municipal ou privé"
    NURSERY = 4, "Etablissement accueil petite enfance"
    RESTAURANT = 5, "Restauration commerciale en continu"


class Building(models.Model):
    name = models.CharField(max_length=100, help_text="The name of this building")
    usage = models.IntegerField(
        choices=Usage.choices, help_text="The usage of this building"
    )
    reference_period = models.PositiveIntegerField(
        help_text="The period in years of the lifecycle analysis"
    )

    def impact(self) -> Decimal:
        total_impact = Decimal("0")
        for zone in self.zones.all():
            zone_impact = sum(zone.impacts())
            total_impact += zone_impact

        return total_impact

    def __str__(self):
        return self.name


class ConstructionProduct(models.Model):
    name = models.CharField(max_length=100, help_text="The name of the product")
    unite = models.CharField(max_length=100, choices=UNITES)
    # Carbon impact
    production_impact = models.DecimalField(max_digits=9, decimal_places=2)
    construction_impact = models.DecimalField(max_digits=9, decimal_places=2)
    exploitation_impact = models.DecimalField(max_digits=9, decimal_places=2)
    endoflife_impact = models.DecimalField(max_digits=9, decimal_places=2)

    typical_lifetime = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def impact_production(self, quantity: Decimal) -> Decimal:
        return self.production_impact * quantity

    def impact_construction(self, quantity: Decimal) -> Decimal:
        return self.construction_impact * quantity

    def impact_endoflife(self, quantity: Decimal) -> Decimal:
        return self.endoflife_impact * quantity

    def impacts(self, quantity: Decimal) -> tuple[Decimal, Decimal, Decimal]:
        return (
            self.impact_production(quantity),
            self.impact_construction(quantity),
            self.impact_endoflife(quantity),
        )


class Zone(models.Model):
    name = models.CharField(max_length=100, help_text="The name of this zone")
    building = models.ForeignKey(
        to=Building, related_name="zones", null=False, on_delete=models.CASCADE
    )
    surface = models.DecimalField(max_digits=9, decimal_places=2)
    usage = models.IntegerField(
        choices=Usage.choices, help_text="The usage of this zone"
    )

    products = models.ManyToManyField(ConstructionProduct, through="ZoneProduct")

    def impacts(self) -> tuple[Decimal, Decimal, Decimal]:
        zone_products = ZoneProduct.objects.all().filter(zone=self)
        products_impacts = [
            zone_product.product.impacts(zone_product.quantity)
            for zone_product in zone_products
        ]
        production_impacts, construction_impacts, endoflife_impacts = list(
            zip(*products_impacts)
        )

        return (
            sum(production_impacts),
            sum(construction_impacts),
            sum(endoflife_impacts),
        )

    def __str__(self):
        return self.name


class ZoneProduct(models.Model):
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE)
    product = models.ForeignKey(to=ConstructionProduct, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=9, decimal_places=2)
