import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, ships):
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
