# Generated by Django 4.2.6 on 2023-10-20 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Building",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of this building", max_length=100
                    ),
                ),
                (
                    "usage",
                    models.IntegerField(
                        choices=[
                            (1, "Logement collectif"),
                            (2, "Bureaux"),
                            (3, "Etablissement sportif municipal ou privé"),
                            (4, "Etablissement accueil petite enfance"),
                            (5, "Restauration commerciale en continu"),
                        ],
                        help_text="The usage of this building",
                    ),
                ),
                (
                    "reference_period",
                    models.PositiveIntegerField(
                        help_text="The period in years of the lifecycle analysis"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ConstructionProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of the product", max_length=100
                    ),
                ),
                (
                    "unite",
                    models.CharField(
                        choices=[
                            ("KG", "Kilogram"),
                            ("M", "Meter"),
                            ("M2", "Square meter"),
                            ("mL", "Linear meter"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "production_impact",
                    models.DecimalField(decimal_places=2, max_digits=9),
                ),
                (
                    "construction_impact",
                    models.DecimalField(decimal_places=2, max_digits=9),
                ),
                (
                    "exploitation_impact",
                    models.DecimalField(decimal_places=2, max_digits=9),
                ),
                (
                    "endoflife_impact",
                    models.DecimalField(decimal_places=2, max_digits=9),
                ),
                ("typical_lifetime", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Zone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="The name of this zone", max_length=100),
                ),
                ("surface", models.DecimalField(decimal_places=2, max_digits=9)),
                (
                    "usage",
                    models.IntegerField(
                        choices=[
                            (1, "Logement collectif"),
                            (2, "Bureaux"),
                            (3, "Etablissement sportif municipal ou privé"),
                            (4, "Etablissement accueil petite enfance"),
                            (5, "Restauration commerciale en continu"),
                        ],
                        help_text="The usage of this zone",
                    ),
                ),
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zones",
                        to="vizcab.building",
                    ),
                ),
            ],
        ),
    ]
