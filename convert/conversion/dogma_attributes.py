import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path):
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
    def add_esf_attribute(id, name, high_is_good):
        pb2.entries[id].name = name
        pb2.entries[id].published = True
        pb2.entries[id].defaultValue = 0
        pb2.entries[id].highIsGood = high_is_good
        pb2.entries[id].stackable = False

    add_esf_attribute(-1, "alignTime", False)
    add_esf_attribute(-2, "scanStrength", True)
    add_esf_attribute(-3, "cpuUsed", False)
    add_esf_attribute(-4, "powerUsed", False)
    add_esf_attribute(-5, "cpuUnused", True)
    add_esf_attribute(-6, "powerUnused", True)
    add_esf_attribute(-7, "velocityBoost", True)
    add_esf_attribute(-8, "shieldEhpMultiplier", True)
    add_esf_attribute(-9, "armorEhpMultiplier", True)
    add_esf_attribute(-10, "hullEhpMultiplier", True)
    add_esf_attribute(-11, "shieldEhp", True)
    add_esf_attribute(-12, "armorEhp", True)
    add_esf_attribute(-13, "hullEhp", True)
    add_esf_attribute(-14, "ehp", True)
    add_esf_attribute(-15, "passiveShieldRecharge", True)
    add_esf_attribute(-16, "shieldBoostRate", True)
    add_esf_attribute(-17, "armorRepairRate", True)
    add_esf_attribute(-18, "hullRepairRate", True)
    add_esf_attribute(-19, "passiveShieldRechargeEhp", True)
    add_esf_attribute(-20, "shieldBoostRateEhp", True)
    add_esf_attribute(-21, "armorRepairRateEhp", True)
    add_esf_attribute(-22, "hullRepairRateEhp", True)
    add_esf_attribute(-23, "capacitorPeakRecharge", True)
    add_esf_attribute(-24, "capacitorPeakUsage", False)
    add_esf_attribute(-25, "capacitorPeakDelta", True)
    add_esf_attribute(-26, "capacitorPeakDeltaPercentage", True)
    add_esf_attribute(-27, "capacitorDepletesIn", False)
    add_esf_attribute(-28, "damageWithoutReloadDps", True)
    add_esf_attribute(-29, "damageWithReloadDps", True)
    add_esf_attribute(-30, "damageAlphaHp", True)
    add_esf_attribute(-31, "droneActive", True)
    add_esf_attribute(-32, "droneBandwidthUsedTotal", False)
    add_esf_attribute(-33, "droneDamageAlphaHp", True)
    add_esf_attribute(-34, "droneDamageDps", True)
    add_esf_attribute(-35, "droneCapacityUsed", False)

    with open("dist/sde/dogmaAttributes.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/dogmaAttributes.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
