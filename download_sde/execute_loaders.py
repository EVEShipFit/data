import pickle
import glob
import importlib
import json
import os
import sys

sys.path.append("pyd")
os.makedirs("json")


def decode_cfsd(key, data, strings):
    data_type = type(data)

    if data_type.__module__ == "cfsd" and data_type.__name__ == "dict":
        return {k: decode_cfsd(k, v, strings) for k, v in data.items()}
    if data_type.__module__.endswith("Loader"):
        return {x: decode_cfsd(x, getattr(data, x), strings) for x in dir(data) if not x.startswith("__")}

    if data_type.__module__ == "cfsd" and data_type.__name__ == "list":
        return [decode_cfsd(None, v, strings) for v in data]
    if isinstance(data, tuple):
        return tuple([decode_cfsd(None, v, strings) for v in data])

    if data_type.__name__.endswith("_vector"):
        # TODO
        return None

    if isinstance(data, int) or data_type.__name__ == "long":
        # In case it is a NameID, look up the name.
        if key is not None and isinstance(key, str) and key.lower().endswith("nameid") and key != "dungeonNameID":
            return strings[data][0]
        return data
    if isinstance(data, float):
        return data
    if isinstance(data, str):
        return data

    raise ValueError("Unknown type: " + str(type(data)))


# Load all the english strings.
print("Loading 'localization_fsd_en-us.pickle' ...")
with open("data/localization_fsd_en-us.pickle", "rb") as f:
    strings = pickle.load(f)[1]


# Convert all available fsdbinary files via their Loader to JSON.
for loader in glob.glob("pyd/*Loader.pyd"):
    loader_name = os.path.splitext(os.path.basename(loader))[0]
    data_name = loader_name.replace("Loader", "").lower() + ".fsdbinary"

    print("Loading '" + data_name + "' with '" + loader_name + "' ...")

    lib = importlib.import_module(loader_name)
    data = lib.load("data/" + data_name)
    data = decode_cfsd(None, data, strings)

    with open("json/" + data_name.replace(".fsdbinary", ".json"), "w") as f:
        json.dump(data, f, indent=4)
