"""Hand-curated, conservative SC2 entity classification for M11 build-order / economy."""

from __future__ import annotations

# Blizzard internal type name -> M11 category (narrow; unknowns reported separately).
ENTITY_CATEGORY: dict[str, str] = {
    # Terran workers / core
    "SCV": "worker",
    "MULE": "worker",
    # Protoss
    "Probe": "worker",
    # Zerg
    "Drone": "worker",
    # Terran townhalls
    "CommandCenter": "townhall",
    "OrbitalCommand": "townhall",
    "PlanetaryFortress": "townhall",
    # Protoss
    "Nexus": "townhall",
    # Zerg
    "Hatchery": "townhall",
    "Lair": "townhall",
    "Hive": "townhall",
    # Gas
    "Refinery": "gas_structure",
    "Assimilator": "gas_structure",
    "Extractor": "gas_structure",
    # Supply
    "SupplyDepot": "supply_provider",
    "SupplyDepotLowered": "supply_provider",
    "Pylon": "supply_provider",
    "Overlord": "supply_provider",
    "Overseer": "supply_provider",
    # Terran production
    "Barracks": "production_structure",
    "Factory": "production_structure",
    "Starport": "production_structure",
    "GhostAcademy": "production_structure",
    "FusionCore": "production_structure",
    "Armory": "tech_structure",
    "EngineeringBay": "tech_structure",
    "TechLab": "production_structure",
    "Reactor": "production_structure",
    # Protoss production
    "Gateway": "production_structure",
    "WarpGate": "production_structure",
    "RoboticsFacility": "production_structure",
    "RoboticsBay": "production_structure",
    "Stargate": "production_structure",
    "DarkShrine": "production_structure",
    "Forge": "tech_structure",
    "CyberneticsCore": "tech_structure",
    "TemplarArchive": "tech_structure",
    "FleetBeacon": "tech_structure",
    "TwilightCouncil": "tech_structure",
    # Zerg production
    "SpawningPool": "production_structure",
    "RoachWarren": "production_structure",
    "HydraliskDen": "production_structure",
    "Spire": "production_structure",
    "NydusNetwork": "production_structure",
    "InfestationPit": "production_structure",
    "UltraliskCavern": "production_structure",
    "LurkerDen": "production_structure",
    "BanelingNest": "production_structure",
    "EvolutionChamber": "tech_structure",
    # Combat units (explicitly catalogued as combat_or_other for M11; not economy claims)
    "Marine": "combat_or_other",
    "Marauder": "combat_or_other",
    "Zergling": "combat_or_other",
    "Zealot": "combat_or_other",
}

# Upgrade internal name -> category (economy upgrade vs tech upgrade).
UPGRADE_CATEGORY: dict[str, str] = {
    "Stimpack": "tech_upgrade",
    "InfantryWeaponsLevel1": "tech_upgrade",
    "InfantryArmorLevel1": "tech_upgrade",
    "ProtossGroundWeaponsLevel1": "tech_upgrade",
    "ProtossGroundArmorLevel1": "tech_upgrade",
    "ZergMeleeWeaponsLevel1": "tech_upgrade",
    "ZergGroundArmorLevel1": "tech_upgrade",
    "MetabolicBoost": "tech_upgrade",
    "GroovedSpines": "tech_upgrade",
    "HiSecAutoTracking": "economy_upgrade",
}

# Curated morph destinations (unit_type_changed) -> category for the *destination* type.
MORPH_DESTINATION_CATEGORY: dict[str, str] = {
    "WarpGate": "production_structure",
    "Lair": "townhall",
    "Hive": "townhall",
    "OrbitalCommand": "townhall",
    "PlanetaryFortress": "townhall",
    "Baneling": "combat_or_other",
    "Ravager": "combat_or_other",
}

STRUCTURE_CATEGORIES: frozenset[str] = frozenset(
    {
        "townhall",
        "gas_structure",
        "supply_provider",
        "production_structure",
        "tech_structure",
    },
)
