import json
import yaml

import esf_pb2

from google.protobuf.json_format import MessageToJson


def convert(path, data, patches):
    print("Loading typeDogma ...")

    try:
        with open(f"{path}/typeDogma.yaml") as fp:
            typeDogma = yaml.load(fp, Loader=yaml.CSafeLoader)
    except FileNotFoundError:
        with open(f"{path}/typedogma.json") as fp:
            typeDogma = json.load(fp)
            typeDogma = {int(k): v for k, v in typeDogma.items()}

    data["typeDogma"] = typeDogma
    yield

    print("Converting typeDogma ...")

    pb2 = esf_pb2.TypeDogma()

    for id, entry in typeDogma.items():
        for attribute in entry["dogmaAttributes"]:
            pbea = pb2.TypeDogmaEntry.DogmaAttributes(attributeID=attribute["attributeID"], value=attribute["value"])

            pb2.entries[id].dogmaAttributes.append(pbea)

        for effect in entry["dogmaEffects"]:
            pbee = pb2.TypeDogmaEntry.DogmaEffects(effectID=effect["effectID"], isDefault=effect["isDefault"])

            pb2.entries[id].dogmaEffects.append(pbee)

    with open("dist/sde/typeDogma.pb2", "wb") as fp:
        fp.write(pb2.SerializeToString())

    with open("dist/sde_json/typeDogma.json", "w") as fp:
        fp.write(MessageToJson(pb2, sort_keys=True))
