import json
from decimal import Decimal
from typing import TypedDict

from vizcab import models

BUILDING_DATA_FILE = "../data/batiments.json"
CONSTRUCTION_ELEMENTS_FILE = "../data/construction_elements.json"
ZONE_DATA_FILE = "../data/zones.json"


UNITES = {
    "kg": "KG",
    "m": "M",
    "m²": "M2",
    "mL": "ML",
}


class BuildingSchema(TypedDict):
    id: int
    nom: str
    surface: None
    zoneIds: list[int]
    usage: None
    periodeDeReference: int


def import_building():
    with open(BUILDING_DATA_FILE, "r") as fd:
        data = fd.read()

    buildings: list[BuildingSchema] = json.loads(data)
    building_instances = [
        models.Building(
            pk=building["id"],
            name=building["nom"],
            reference_period=building["periodeDeReference"],
        )
        for building in buildings
    ]
    models.Building.objects.bulk_create(building_instances, ignore_conflicts=True)


class ImpactSchema(TypedDict):
    production: Decimal
    construction: Decimal
    exploitation: Decimal
    finDeVie: Decimal


class ConstructionElementSchema(TypedDict):
    id: int
    nom: str
    unite: str
    impactUnitaireRechauffementClimatique: ImpactSchema
    dureeVieTypique: Decimal


def import_construction_element():
    with open(CONSTRUCTION_ELEMENTS_FILE, "r") as fd:
        data = fd.read()

    constructions_elements: list[ConstructionElementSchema] = json.loads(data)

    constructions_elements_instances = [
        models.ConstructionProduct(
            pk=element["id"],
            name=element["nom"],
            unite=UNITES[element["unite"]],
            production_impact=element["impactUnitaireRechauffementClimatique"][
                "production"
            ],
            construction_impact=element["impactUnitaireRechauffementClimatique"][
                "construction"
            ],
            exploitation_impact=element["impactUnitaireRechauffementClimatique"][
                "exploitation"
            ],
            endoflife_impact=element["impactUnitaireRechauffementClimatique"][
                "finDeVie"
            ],
            typical_lifetime=element["dureeVieTypique"],
        )
        for element in constructions_elements
    ]
    models.ConstructionProduct.objects.bulk_create(
        constructions_elements_instances, ignore_conflicts=True
    )


class ZoneElementSchema(TypedDict):
    id: int
    quantite: Decimal


class ZoneSchema(TypedDict):
    id: int
    nom: str
    usage: int
    constructionElements: list[ZoneElementSchema]


def import_zones():
    with open(ZONE_DATA_FILE, "r") as fd:
        data = fd.read()
    zones: list[ZoneSchema] = json.loads(data)

    with open(BUILDING_DATA_FILE, "r") as fd:
        data = fd.read()
    buildings: list[BuildingSchema] = json.loads(data)

    zones_building = {
        zone_id: building["id"]
        for building in buildings
        for zone_id in building["zoneIds"]
    }

    for zone in zones:
        building = models.Building.objects.get(pk=zones_building[zone["id"]])
        zone_instance, _ = models.Zone.objects.get_or_create(
            id=zone["id"],
            defaults={
                "name": zone["nom"],
                "building": building,
                "surface": zone["surface"],
                "usage": zone["usage"],
            },
        )

        for elements in zone["constructionElements"]:
            element_instance = models.ConstructionProduct.objects.get(pk=elements["id"])
            models.ZoneProduct.objects.get_or_create(
                zone=zone_instance,
                product=element_instance,
                defaults={"quantity": elements["quantite"]},
            )


def run():
    import_building()
    import_construction_element()
    import_zones()
