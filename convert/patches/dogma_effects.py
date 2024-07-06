effectCategoryNameToId = {
    "passive": 0,
    "active": 1,
    "target": 2,
    "area": 3,
    "online": 4,
    "overload": 5,
    "dungeon": 6,
    "system": 7,
}

effectOperationNameToId = {
    "preAssign": -1,
    "preMul": 0,
    "preDiv": 1,
    "modAdd": 2,
    "modSub": 3,
    "postMul": 4,
    "postDiv": 5,
    "postPercent": 6,
    "postAssign": 7,
    # 8 is not used.
    # 9 is related to SkillLevel calculation, which is unused.
}


def _fixup_modifier_info(modifier, data):
    if "modifiedAttribute" in modifier:
        try:
            modifier["modifiedAttributeID"] = [
                id
                for id, attribute in data["dogmaAttributes"].items()
                if attribute["name"] == modifier["modifiedAttribute"]
            ][0]
        except IndexError:
            raise ValueError(f"Unknown attribute: {modifier['modifiedAttribute']}")
        del modifier["modifiedAttribute"]
    if "modifyingAttribute" in modifier:
        try:
            modifier["modifyingAttributeID"] = [
                id
                for id, attribute in data["dogmaAttributes"].items()
                if attribute["name"] == modifier["modifyingAttribute"]
            ][0]
        except IndexError:
            raise ValueError(f"Unknown attribute: {modifier['modifyingAttribute']}")
        del modifier["modifyingAttribute"]
    if "skillType" in modifier:
        if modifier["skillType"] == "IfSkillRequired":
            modifier["skillTypeID"] = -1
        else:
            try:
                modifier["skillTypeID"] = [
                    id for id, skill in data["types"].items() if skill["name"] == modifier["skillType"]
                ][0]
            except IndexError:
                raise ValueError(f"Unknown skill: {modifier['skillType']}")
        del modifier["skillType"]
    if "operation" in modifier:
        modifier["operation"] = effectOperationNameToId[modifier["operation"]]


def patch(entries, patches, data):
    nextEffectID = -1
    for patch in patches:
        # Lookup fields that require lookup.
        if "effectCategory" in patch:
            patch["effectCategory"] = effectCategoryNameToId[patch["effectCategory"]]
        for modifier in patch.get("modifierInfo", []):
            _fixup_modifier_info(modifier, data)

        # Add new entries.
        if patch.get("new"):
            patch["effectName"] = patch["new"]["name"]
            del patch["new"]

            # Check if the name is unique.
            for entry in entries.values():
                if entry["effectName"] == patch["effectName"]:
                    raise ValueError(f"Effect name '{patch['effectName']}' is not unique.")

            entries[nextEffectID] = patch
            nextEffectID -= 1

        # Fixup patch entries.
        if patch.get("patch"):
            names = [patchTarget["name"] for patchTarget in patch["patch"]]
            effectIDs = [id for id, entry in entries.items() if entry["effectName"] in names]

            # Append the modifierInfo.
            for modifier in patch.get("modifierInfo", []):
                for effectID in effectIDs:
                    if "modifierInfo" not in entries[effectID]:
                        entries[effectID]["modifierInfo"] = []
                    entries[effectID]["modifierInfo"].append(modifier)

            del patch["patch"]
            if "modifierInfo" in patch:
                del patch["modifierInfo"]

            # Update any remaining fields.
            for effectID in effectIDs:
                entries[effectID].update(patch)
