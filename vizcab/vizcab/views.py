from rest_framework import viewsets
from django.db.models import Sum, Q, Case, Value, When, F
from django.db.models.functions import Greatest

from . import serializers
from . import models


class Building(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.Building
    queryset = models.Building.objects.all()

    def get_queryset(self):
        # TODO This one is very long and static wich each usage listed
        # We may make this generic based on a list of usage

        queryset = models.Building.objects.all()

        # Add total surfaces and surfaces of each zones of this building
        queryset = queryset.annotate(
            surface=Sum("zones__surface", default=0.0),
            housing_surface=Sum(
                "zones__surface",
                default=0.0,
                filter=Q(zones__usage=models.Usage.HOUSING),
            ),
            gymnasium_surface=Sum(
                "zones__surface",
                default=0.0,
                filter=Q(zones__usage=models.Usage.GYMNASIUM),
            ),
            office_surface=Sum(
                "zones__surface",
                default=0.0,
                filter=Q(zones__usage=models.Usage.OFFICES),
            ),
            nursery_surface=Sum(
                "zones__surface",
                default=0.0,
                filter=Q(zones__usage=models.Usage.NURSERY),
            ),
            restaurant_surface=Sum(
                "zones__surface",
                default=0.0,
                filter=Q(zones__usage=models.Usage.RESTAURANT),
            ),
        )

        # Add the most bigger surface of each zones
        queryset = queryset.annotate(
            max_surface_zone=Greatest(
                "housing_surface",
                "gymnasium_surface",
                "office_surface",
                "nursery_surface",
                "restaurant_surface",
            )
        )

        # Add the bigger usage, comparing the max_surface_zone to each zones surface
        queryset = queryset.annotate(
            most_usage=Case(
                When(
                    max_surface_zone=0.0,
                    then=Value(""),
                ),
                When(
                    max_surface_zone=F("housing_surface"),
                    then=Value(models.Usage.HOUSING.name),
                ),
                When(
                    max_surface_zone=F("gymnasium_surface"),
                    then=Value(models.Usage.GYMNASIUM.name),
                ),
                When(
                    max_surface_zone=F("office_surface"),
                    then=Value(models.Usage.OFFICES.name),
                ),
                When(
                    max_surface_zone=F("nursery_surface"),
                    then=Value(models.Usage.NURSERY.name),
                ),
                When(
                    max_surface_zone=F("restaurant_surface"),
                    then=Value(models.Usage.RESTAURANT.name),
                ),
                default=Value(""),
            ),
        )

        return queryset
