import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path):
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
