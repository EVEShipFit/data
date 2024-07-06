import glob
import yaml


def load_patches():
    effects = []
    attributes = []
    typeDogma = []

    for patch in sorted(glob.glob("patches/*.yaml")):
        with open(patch) as fp:
            patch = yaml.load(fp, Loader=yaml.CSafeLoader)

        for attribute in patch.get("attributes", []):
            attributes.append(attribute)

        for effect in patch.get("effects", []):
            effects.append(effect)

        for entry in patch.get("typeDogma", []):
            typeDogma.append(entry)

    return {
        "effects": effects,
        "attributes": attributes,
        "typeDogma": typeDogma,
    }
