def _fixup_attribute(attribute, data):
    try:
        attribute["attributeID"] = [
            id for id, item in data["dogmaAttributes"].items() if item["name"] == attribute["attribute"]
        ][0]
    except IndexError:
        raise ValueError(f"Unknown attribute: {attribute['attribute']}")
    del attribute["attribute"]


def _fixup_effect(effect, data):
    try:
        effect["effectID"] = [
            id for id, item in data["dogmaEffects"].items() if item["effectName"] == effect["effect"]
        ][0]
    except IndexError:
        raise ValueError(f"Unknown attribute: {effect['effect']}")
    del effect["effect"]


def patch(entries, patches, data):
    for patch in patches:
        # Lookup fields that require lookup.
        for attribute in patch.get("dogmaAttributes", []):
            _fixup_attribute(attribute, data)
        for effect in patch.get("dogmaEffects", []):
            _fixup_effect(effect, data)

        appliedIDs = set()

        # Fixup patch entries.
        for patchTarget in patch.get("patch", []):
            if "category" in patchTarget:
                try:
                    categoryID = [
                        id for id, category in data["categories"].items() if category["name"] == patchTarget["category"]
                    ][0]
                except IndexError:
                    raise ValueError(f"Unknown category: {patchTarget['category']}")

                groupIDs = [id for id, item in data["groups"].items() if item["categoryID"] == categoryID]
                typeIDs = [id for id, item in data["types"].items() if item["groupID"] in groupIDs]
            elif "type" in patchTarget:
                try:
                    typeIDs = [id for id, item in data["types"].items() if item["name"] == patchTarget["type"]]
                except IndexError:
                    raise ValueError(f"Unknown type: {patchTarget['type']}")
            else:
                raise ValueError("Unknown patch type")

            # Ensure there is a dogma entry for each type.
            for typeID in typeIDs:
                if typeID not in entries:
                    entries[typeID] = {
                        "dogmaAttributes": [],
                        "dogmaEffects": [],
                    }

            if "hasAllAttributes" in patchTarget:
                for attribute in patchTarget["hasAllAttributes"]:
                    try:
                        attributeID = [
                            id for id, item in data["dogmaAttributes"].items() if item["name"] == attribute["name"]
                        ][0]
                    except IndexError:
                        raise ValueError(f"Unknown attribute: {attribute['name']}")

                    filteredTypeIDs = []
                    for typeID in typeIDs:
                        if attributeID in [
                            attribute["attributeID"] for attribute in entries[typeID]["dogmaAttributes"]
                        ]:
                            filteredTypeIDs.append(typeID)

                    typeIDs = filteredTypeIDs

            if "hasAnyAttributes" in patchTarget:
                filteredTypeIDs = []

                for attribute in patchTarget["hasAnyAttributes"]:
                    try:
                        attributeID = [
                            id for id, item in data["dogmaAttributes"].items() if item["name"] == attribute["name"]
                        ][0]
                    except IndexError:
                        raise ValueError(f"Unknown attribute: {attribute['name']}")

                    for typeID in typeIDs:
                        if attributeID in [
                            attribute["attributeID"] for attribute in entries[typeID]["dogmaAttributes"]
                        ]:
                            filteredTypeIDs.append(typeID)

                typeIDs = filteredTypeIDs

            if "hasAnyEffects" in patchTarget:
                filteredTypeIDs = []

                for effect in patchTarget["hasAnyEffects"]:
                    try:
                        effectID = [
                            id for id, item in data["dogmaEffects"].items() if item["effectName"] == effect["name"]
                        ][0]
                    except IndexError:
                        raise ValueError(f"Unknown effect: {effect['name']}")

                    for typeID in typeIDs:
                        if effectID in [effect["effectID"] for effect in entries[typeID]["dogmaEffects"]]:
                            filteredTypeIDs.append(typeID)

                typeIDs = filteredTypeIDs

            # Ensure we never apply the same effect twice on the same type.
            typeIDs = list(set(typeIDs) - appliedIDs)

            # Append dogmaAttributes.
            for attribute in patch.get("dogmaAttributes", []):
                for typeID in typeIDs:
                    entries[typeID]["dogmaAttributes"].append(attribute)

            # Append dogmaEffects.
            for effect in patch.get("dogmaEffects", []):
                for typeID in typeIDs:
                    entries[typeID]["dogmaEffects"].append(effect)

            appliedIDs.update(typeIDs)
