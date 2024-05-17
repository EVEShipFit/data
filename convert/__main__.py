import json
import os
import sys
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson

if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist/sde", exist_ok=True)
os.makedirs("dist/sde_json", exist_ok=True)


def convert_type_dogma(path, ships):
    print("Converting typeDogma ...")

    try:
        with open(f"{path}/typeDogma.yaml") as fp:
            typeDogma = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/typedogma.json") as fp:
            typeDogma = json.load(fp)
            typeDogma = {int(k): v for k, v in typeDogma.items()}

    pb2 = esf_pb2.TypeDogma()

    for id, entry in typeDogma.items():
        for attribute in entry["dogmaAttributes"]:
            pbea = pb2.TypeDogmaEntry.DogmaAttributes(attributeID=attribute["attributeID"], value=attribute["value"])

            pb2.entries[id].dogmaAttributes.append(pbea)

        for effect in entry["dogmaEffects"]:
            pbee = pb2.TypeDogmaEntry.DogmaEffects(effectID=effect["effectID"], isDefault=effect["isDefault"])

            pb2.entries[id].dogmaEffects.append(pbee)

        if id in ships:
            # Add the "applyVelocityBoost" effect for all ships.
            pbee = pb2.TypeDogmaEntry.DogmaEffects(effectID=-1, isDefault=False)
            pb2.entries[id].dogmaEffects.append(pbee)

        if id == 1373:  # 1373 - Character
            # Add the "applyMissileDamage" effect for chars.
            pbee = pb2.TypeDogmaEntry.DogmaEffects(effectID=-2, isDefault=False)
            pb2.entries[id].dogmaEffects.append(pbee)

    with open("dist/sde/typeDogma.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/typeDogma.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))


def convert_type_ids(path):
    print("Converting typeIDs ...")

    try:
        with open(f"{path}/groupIDs.yaml") as fp:
            groupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/groups.json") as fp:
            groupIDs = json.load(fp)
            groupIDs = {int(k): v for k, v in groupIDs.items()}

    try:
        with open(f"{path}/typeIDs.yaml") as fp:
            typeIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/types.json") as fp:
            typeIDs = json.load(fp)
            typeIDs = {int(k): v for k, v in typeIDs.items()}

    pb2 = esf_pb2.TypeIDs()
    ships = []

    for id, entry in typeIDs.items():
        pb2.entries[id].name = entry["name"]["en"] if "name" in entry else entry["typeNameID"]
        pb2.entries[id].groupID = entry["groupID"]
        pb2.entries[id].categoryID = groupIDs[entry["groupID"]]["categoryID"]
        pb2.entries[id].published = entry["published"]

        if groupIDs[entry["groupID"]]["categoryID"] == 6:
            ships.append(id)

        if "factionID" in entry:
            pb2.entries[id].factionID = entry["factionID"]
        if "marketGroupID" in entry:
            pb2.entries[id].marketGroupID = entry["marketGroupID"]
        if "metaGroupID" in entry:
            pb2.entries[id].metaGroupID = entry["metaGroupID"]
        if "capacity" in entry and entry["capacity"] != 0.0:
            pb2.entries[id].capacity = entry["capacity"]
        if "mass" in entry and entry["mass"] != 0.0:
            pb2.entries[id].mass = entry["mass"]
        if "radius" in entry and entry["radius"] != 1.0:
            pb2.entries[id].radius = entry["radius"]
        if "volume" in entry and entry["volume"] != 0.0:
            pb2.entries[id].volume = entry["volume"]

    with open("dist/sde/typeIDs.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/typeIDs.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))

    return ships


def convert_group_ids(path):
    print("Converting groupIDs ...")

    try:
        with open(f"{path}/groupIDs.yaml") as fp:
            groupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/groups.json") as fp:
            groupIDs = json.load(fp)
            groupIDs = {int(k): v for k, v in groupIDs.items()}

    pb2 = esf_pb2.GroupIDs()

    for id, entry in groupIDs.items():
        pb2.entries[id].name = entry["name"]["en"] if "name" in entry else entry["groupNameID"]
        pb2.entries[id].categoryID = entry["categoryID"]
        pb2.entries[id].published = entry["published"]

    with open("dist/sde/groupIDs.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/groupIDs.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))


def convert_market_groups(path):
    print("Converting marketGroups ...")

    try:
        with open(f"{path}/marketGroups.yaml") as fp:
            marketGroupIDs = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/marketgroups.json") as fp:
            marketGroupIDs = json.load(fp)
            marketGroupIDs = {int(k): v for k, v in marketGroupIDs.items()}

    pb2 = esf_pb2.MarketGroups()

    for id, entry in marketGroupIDs.items():
        pb2.entries[id].name = entry["nameID"] if isinstance(entry["nameID"], str) else entry["nameID"]["en"]

        if "parentGroupID" in entry:
            pb2.entries[id].parentGroupID = entry["parentGroupID"]
        if "iconID" in entry:
            pb2.entries[id].iconID = entry["iconID"]

    with open("dist/sde/marketGroups.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/marketGroups.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))


def convert_dogma_attributes(path):
    print("Converting dogmaAttributes ...")

    try:
        with open(f"{path}/dogmaAttributes.yaml") as fp:
            dogmaAttributes = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/dogmaattributes.json") as fp:
            dogmaAttributes = json.load(fp)
            dogmaAttributes = {int(k): v for k, v in dogmaAttributes.items()}

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
        pb2.entries[id].highIsGood = False
        pb2.entries[id].stackable = False

    add_esf_attribute(-1, "alignTime")
    add_esf_attribute(-2, "scanStrength")
    add_esf_attribute(-3, "cpuUsed")
    add_esf_attribute(-4, "powerUsed")
    add_esf_attribute(-5, "cpuUnused")
    add_esf_attribute(-6, "powerUnused")
    add_esf_attribute(-7, "velocityBoost")
    add_esf_attribute(-8, "shieldEhpMultiplier")
    add_esf_attribute(-9, "armorEhpMultiplier")
    add_esf_attribute(-10, "hullEhpMultiplier")
    add_esf_attribute(-11, "shieldEhp")
    add_esf_attribute(-12, "armorEhp")
    add_esf_attribute(-13, "hullEhp")
    add_esf_attribute(-14, "ehp")
    add_esf_attribute(-15, "passiveShieldRecharge")
    add_esf_attribute(-16, "shieldBoostRate")
    add_esf_attribute(-17, "armorRepairRate")
    add_esf_attribute(-18, "hullRepairRate")
    add_esf_attribute(-19, "passiveShieldRechargeEhp")
    add_esf_attribute(-20, "shieldBoostRateEhp")
    add_esf_attribute(-21, "armorRepairRateEhp")
    add_esf_attribute(-22, "hullRepairRateEhp")
    add_esf_attribute(-23, "capacitorPeakRecharge")
    add_esf_attribute(-24, "capacitorPeakUsage")
    add_esf_attribute(-25, "capacitorPeakDelta")
    add_esf_attribute(-26, "capacitorPeakDeltaPercentage")
    add_esf_attribute(-27, "capacitorDepletesIn")
    add_esf_attribute(-28, "damageWithoutReloadDps")
    add_esf_attribute(-29, "damageWithReloadDps")
    add_esf_attribute(-30, "damageAlphaHp")
    add_esf_attribute(-31, "droneActive")
    add_esf_attribute(-32, "droneBandwidthUsedTotal")
    add_esf_attribute(-33, "droneDamageAlphaHp")
    add_esf_attribute(-34, "droneDamageDps")
    add_esf_attribute(-35, "droneCapacityUsed")

    with open("dist/sde/dogmaAttributes.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/dogmaAttributes.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))


def convert_dogma_effects(path):
    print("Converting dogmaEffects ...")

    try:
        with open(f"{path}/dogmaEffects.yaml") as fp:
            dogmaEffects = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/dogmaeffects.json") as fp:
            dogmaEffects = json.load(fp)
            dogmaEffects = {int(k): v for k, v in dogmaEffects.items()}

    pb2 = esf_pb2.DogmaEffects()
    pbmi = pb2.DogmaEffect.ModifierInfo()

    def add_modifier(id, domain, func, modifiedAttributeID, operation, modifyingAttributeID, **kwargs):
        pbmi = pb2.DogmaEffect.ModifierInfo()

        pbmi.domain = domain
        pbmi.func = func
        pbmi.modifiedAttributeID = modifiedAttributeID
        pbmi.modifyingAttributeID = modifyingAttributeID
        pbmi.operation = operation

        for key, value in kwargs.items():
            setattr(pbmi, key, value)

        pb2.entries[id].modifierInfo.append(pbmi)

    # Add the "applyVelocityBoost" effect.
    pb2.entries[-1].name = "applyVelocityBoost"
    pb2.entries[-1].effectCategory = 0
    pb2.entries[-1].electronicChance = 0
    pb2.entries[-1].isAssistance = False
    pb2.entries[-1].isOffensive = False
    pb2.entries[-1].isWarpSafe = True
    pb2.entries[-1].propulsionChance = 0
    pb2.entries[-1].rangeChance = 0

    # Final step of applying the velocity bonus.
    add_modifier(-1, pbmi.Domain.itemID, pbmi.Func.ItemModifier, -7, 5, 4)  # velocityBoost <postDiv> mass
    add_modifier(-1, pbmi.Domain.itemID, pbmi.Func.ItemModifier, 37, 6, -7)  # maxVelocity <postPercent> velocityBoost

    # Add the "applyMissileDamage" effect.
    pb2.entries[-2].name = "applyMissileDamage"
    pb2.entries[-2].effectCategory = 0
    pb2.entries[-2].electronicChance = 0
    pb2.entries[-2].isAssistance = False
    pb2.entries[-2].isOffensive = True
    pb2.entries[-2].isWarpSafe = True
    pb2.entries[-2].propulsionChance = 0
    pb2.entries[-2].rangeChance = 0

    add_modifier(
        -2, pbmi.Domain.charID, pbmi.Func.OwnerRequiredSkillModifier, 114, 4, 212, skillTypeID=3319
    )  # emDamage <postMul> missileDamageMultiplier for Missile Launcher Operation skill
    add_modifier(
        -2, pbmi.Domain.charID, pbmi.Func.OwnerRequiredSkillModifier, 116, 4, 212, skillTypeID=3319
    )  # explosiveDamage <postMul> missileDamageMultiplier for Missile Launcher Operation skill
    add_modifier(
        -2, pbmi.Domain.charID, pbmi.Func.OwnerRequiredSkillModifier, 117, 4, 212, skillTypeID=3319
    )  # kineticDamage <postMul> missileDamageMultiplier for Missile Launcher Operation skill
    add_modifier(
        -2, pbmi.Domain.charID, pbmi.Func.OwnerRequiredSkillModifier, 118, 4, 212, skillTypeID=3319
    )  # thermalDamage <postMul> missileDamageMultiplier for Missile Launcher Operation skill

    for id, entry in dogmaEffects.items():
        pb2.entries[id].name = entry["effectName"]
        # In the SDE, the "online" effect is in the "active" category.
        # Internally EVE does some magic here; but in our case, it should
        # always be in the "online" category. So change the effect here.
        if entry["effectName"] == "online":
            pb2.entries[id].effectCategory = 4
        else:
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
                    case "itemID":
                        pbmi.domain = pbmi.Domain.itemID
                    case "shipID":
                        pbmi.domain = pbmi.Domain.shipID
                    case "charID":
                        pbmi.domain = pbmi.Domain.charID
                    case "otherID":
                        pbmi.domain = pbmi.Domain.otherID
                    case "structureID":
                        pbmi.domain = pbmi.Domain.structureID
                    case "target":
                        pbmi.domain = pbmi.Domain.target
                    case "targetID":
                        pbmi.domain = pbmi.Domain.targetID

                match modifier_info["func"]:
                    case "ItemModifier":
                        pbmi.func = pbmi.Func.ItemModifier
                    case "LocationGroupModifier":
                        pbmi.func = pbmi.Func.LocationGroupModifier
                    case "LocationModifier":
                        pbmi.func = pbmi.Func.LocationModifier
                    case "LocationRequiredSkillModifier":
                        pbmi.func = pbmi.Func.LocationRequiredSkillModifier
                    case "OwnerRequiredSkillModifier":
                        pbmi.func = pbmi.Func.OwnerRequiredSkillModifier
                    case "EffectStopper":
                        pbmi.func = pbmi.Func.EffectStopper

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

        # In the SDE, the ABs and MWDs don't have an active modifier effect.
        # Internally EVE does some magic here; but in our case, these
        # modifiers can just be assigned to the effects.
        if entry["effectName"] == "moduleBonusMicrowarpdrive":
            add_modifier(
                id, pbmi.Domain.shipID, pbmi.Func.ItemModifier, 552, 6, 554
            )  # signatureRadius <postPercent> signatureRadiusBonus

        if entry["effectName"] == "moduleBonusAfterburner" or entry["effectName"] == "moduleBonusMicrowarpdrive":
            add_modifier(id, pbmi.Domain.shipID, pbmi.Func.ItemModifier, 4, 2, 796)  # mass <modAdd> massAddition

            # Velocity change is calculated like this:
            #   velocityBoost = item.speedFactor * item.speedBoostFactor / ship.mass
            # First, calculate the multiplication on the item.
            add_modifier(
                id, pbmi.Domain.shipID, pbmi.Func.ItemModifier, -7, -1, 567
            )  # velocityBoost <preAssign> speedBoostFactor
            add_modifier(
                id, pbmi.Domain.shipID, pbmi.Func.ItemModifier, -7, 4, 20
            )  # velocityBoost <postMul> speedFactor

            # Next, "applyVelocityBoost" is applied on all ships which takes care of
            # the final calculation (as mass is an attribute of the ship).

        # missileEMDmgBonus, missileExplosiveDmgBonus, missileKineticDmgBonus, missileThermalDmgBonus don't apply
        # any effect direct, but this is handled internally in EVE. For us,
        # it is better to just make it an effect.
        damageType = {
            "missileEMDmgBonus": 114,
            "missileExplosiveDmgBonus": 116,
            "missileKineticDmgBonus2": 117,
            "missileThermalDmgBonus": 118,
        }
        if entry["effectName"] in damageType.keys():
            add_modifier(
                id,
                pbmi.Domain.charID,
                pbmi.Func.OwnerRequiredSkillModifier,
                damageType[entry["effectName"]],
                6,
                292,
                skillTypeID=-1,
            )  # <damageType>Damage <postPercent> damageMultiplierBonus for skill in question.
        if entry["effectName"] == "selfRof":
            add_modifier(
                id, pbmi.Domain.shipID, pbmi.Func.LocationRequiredSkillModifier, 51, 6, 293, skillTypeID=-1
            )  # speed <postPercent> rofBonus for skill in question.
        if entry["effectName"] == "droneDmgBonus":
            add_modifier(
                id, pbmi.Domain.charID, pbmi.Func.OwnerRequiredSkillModifier, 64, 6, 292, skillTypeID=-1
            )  # damageMultiplier <postPercent> damageMultiplierBonus for skill in question.

    with open("dist/sde/dogmaEffects.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/dogmaEffects.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))


convert_group_ids(path)
convert_market_groups(path)
ships = convert_type_ids(path)
convert_type_dogma(path, ships)
convert_dogma_attributes(path)
convert_dogma_effects(path)
