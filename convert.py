import os
import sys
import yaml

import esf_pb2

if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist", exist_ok=True)

def convert_type_dogma(path):
    with open(f"{path}/typeDogma.yaml") as fp:
        typeDogma = yaml.load(fp, Loader=yaml.CSafeLoader)

    pb2 = esf_pb2.TypeDogma()

    for id, entry in typeDogma.items():
        for attribute in entry["dogmaAttributes"]:
            pbea = pb2.TypeDogmaEntry.DogmaAttributes(
                attributeID=attribute["attributeID"],
                value=attribute["value"]
            )

            pb2.entries[id].dogmaAttributes.append(pbea)

        for effect in entry["dogmaEffects"]:
            pbee = pb2.TypeDogmaEntry.DogmaEffects(
                effectID=effect["effectID"],
                isDefault=effect["isDefault"]
            )

            pb2.entries[id].dogmaEffects.append(pbee)

    with open("dist/typeDogma.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())


def convert_type_ids(path):
    with open(f"{path}/groupIDs.yaml") as fp:
        groupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)

    with open(f"{path}/typeIDs.yaml") as fp:
        typeIDs = yaml.load(fp, Loader=yaml.CSafeLoader)

    pb2 = esf_pb2.TypeIDs()

    for id, entry in typeIDs.items():
        pb2.entries[id].name = entry["name"]["en"]
        pb2.entries[id].groupID = entry["groupID"]
        pb2.entries[id].categoryID = groupIDs[entry["groupID"]]["categoryID"]
        pb2.entries[id].published = entry["published"]

        if "marketGroupID" in entry:
            pb2.entries[id].marketGroupID = entry["marketGroupID"]
        if "capacity" in entry:
            pb2.entries[id].capacity = entry["capacity"]
        if "mass" in entry:
            pb2.entries[id].mass = entry["mass"]
        if "radius" in entry:
            pb2.entries[id].radius = entry["radius"]
        if "volume" in entry:
            pb2.entries[id].volume = entry["volume"]

    with open("dist/typeIDs.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())


def convert_dogma_attributes(path):
    with open(f"{path}/dogmaAttributes.yaml") as fp:
        dogmaAttributes = yaml.load(fp, Loader=yaml.CSafeLoader)

    pb2 = esf_pb2.DogmaAttributes()

    for id, entry in dogmaAttributes.items():
        pb2.entries[id].name = entry["name"]
        pb2.entries[id].published = entry["published"]
        pb2.entries[id].defaultValue = entry["defaultValue"]
        pb2.entries[id].highIsGood = entry["highIsGood"]
        pb2.entries[id].stackable = entry["stackable"]

    # Entries that don't exist in the SDE, but are calculated by the library.
    def add_esf_attribute(id, name):
        pb2.entries[id].name = name
        pb2.entries[id].published = True
        pb2.entries[id].defaultValue = 0
        pb2.entries[id].highIsGood = True
        pb2.entries[id].stackable = False

    add_esf_attribute(-1, "alignTime")
    add_esf_attribute(-2, "scanStrength")
    add_esf_attribute(-3, "cpuUsage")
    add_esf_attribute(-4, "powerUsage")

    with open("dist/dogmaAttributes.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())


def convert_dogma_effects(path):
    with open(f"{path}/dogmaEffects.yaml") as fp:
        dogmaEffects = yaml.load(fp, Loader=yaml.CSafeLoader)

    pb2 = esf_pb2.DogmaEffects()

    for id, entry in dogmaEffects.items():
        pb2.entries[id].name = entry["effectName"]
        pb2.entries[id].effectCategory = entry["effectCategory"]
        pb2.entries[id].electronicChance = entry["electronicChance"]
        pb2.entries[id].isAssistance = entry["isAssistance"]
        pb2.entries[id].isOffensive = entry["isOffensive"]
        pb2.entries[id].isWarpSafe = entry["isWarpSafe"]
        pb2.entries[id].propulsionChance = entry["propulsionChance"]
        pb2.entries[id].rangeChance = entry["rangeChance"]

        if "dischargeAttributeID" in entry:
            pb2.entries[id].dischargeAttributeID = entry["dischargeAttributeID"]
        if "durationAttributeID" in entry:
            pb2.entries[id].durationAttributeID = entry["durationAttributeID"]
        if "rangeAttributeID" in entry:
            pb2.entries[id].rangeAttributeID = entry["rangeAttributeID"]
        if "falloffAttributeID" in entry:
            pb2.entries[id].falloffAttributeID = entry["falloffAttributeID"]
        if "trackingSpeedAttributeID" in entry:
            pb2.entries[id].trackingSpeedAttributeID = entry["trackingSpeedAttributeID"]
        if "fittingUsageChanceAttributeID" in entry:
            pb2.entries[id].fittingUsageChanceAttributeID = entry["fittingUsageChanceAttributeID"]
        if "resistanceAttributeID" in entry:
            pb2.entries[id].resistanceAttributeID = entry["resistanceAttributeID"]

        if "modifierInfo" in entry:
            for modifier_info in entry["modifierInfo"]:
                pbmi = pb2.DogmaEffect.ModifierInfo()

                match modifier_info["domain"]:
                    case "itemID": pbmi.domain = pbmi.Domain.itemID
                    case "shipID": pbmi.domain = pbmi.Domain.shipID
                    case "charID": pbmi.domain = pbmi.Domain.charID
                    case "otherID": pbmi.domain = pbmi.Domain.otherID
                    case "structureID": pbmi.domain = pbmi.Domain.structureID
                    case "target": pbmi.domain = pbmi.Domain.target
                    case "targetID": pbmi.domain = pbmi.Domain.targetID

                match modifier_info["func"]:
                    case "ItemModifier": pbmi.func = pbmi.Func.ItemModifier
                    case "LocationGroupModifier": pbmi.func = pbmi.Func.LocationGroupModifier
                    case "LocationModifier": pbmi.func = pbmi.Func.LocationModifier
                    case "LocationRequiredSkillModifier": pbmi.func = pbmi.Func.LocationRequiredSkillModifier
                    case "OwnerRequiredSkillModifier": pbmi.func = pbmi.Func.OwnerRequiredSkillModifier
                    case "EffectStopper": pbmi.func = pbmi.Func.EffectStopper

                if "modifiedAttributeID" in modifier_info:
                    pbmi.modifiedAttributeID = modifier_info["modifiedAttributeID"]
                if "modifyingAttributeID" in modifier_info:
                    pbmi.modifyingAttributeID = modifier_info["modifyingAttributeID"]
                if "operation" in modifier_info:
                    pbmi.operation = modifier_info["operation"]
                if "groupID" in modifier_info:
                    pbmi.groupID = modifier_info["groupID"]
                if "skillTypeID" in modifier_info:
                    pbmi.skillTypeID = modifier_info["skillTypeID"]

                pb2.entries[id].modifierInfo.append(pbmi)

    with open("dist/dogmaEffects.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

convert_type_dogma(path)
convert_type_ids(path)
convert_dogma_attributes(path)
convert_dogma_effects(path)
