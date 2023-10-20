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


class Zone(models.Model):
    name = models.CharField(max_length=100, help_text="The name of this zone")
    building = models.ForeignKey(
        to=Building, related_name="zones", null=False, on_delete=models.CASCADE
    )
    surface = models.DecimalField(max_digits=9, decimal_places=2)
    usage = models.IntegerField(
        choices=Usage.choices, help_text="The usage of this zone"
    )

    def __str__(self):
        return self.name
