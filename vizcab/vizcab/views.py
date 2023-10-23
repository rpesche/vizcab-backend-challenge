from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q, Case, Value, When, F
from django.db.models.functions import Greatest

from . import serializers
from . import models


class Building(viewsets.ReadOnlyModelViewSet):
    queryset = models.Building.objects.all()

    def get_serializer_class(self):
        if self.action == "impacts":
            return serializers.Impacts
        return serializers.Building

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

    @action(detail=True, methods=["get"])
    def impacts(self, request, pk):
        building = self.get_object()

        (
            production_impacts,
            construction_impacts,
            endoflife_impacts,
            exploitation_impact,
        ) = building.impacts()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data={
                "production_impacts": production_impacts.quantize(Decimal("0.01")),
                "construction_impacts": construction_impacts.quantize(Decimal("0.01")),
                "endoflife_impacts": endoflife_impacts.quantize(Decimal("0.01")),
                "exploitation_impact": exploitation_impact.quantize(Decimal("0.01")),
            }
        )

        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
