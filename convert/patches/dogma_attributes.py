def patch(entries, patches, data):
    nextAttributeID = -1

    for patch in patches:
        if patch.get("new"):
            patch["name"] = patch["new"]["name"]
            # Most attributes don't care what number they have; some do.
            nextID = patch["new"]["id"] if "id" in patch["new"] else nextAttributeID
            del patch["new"]

            # Check if the name is unique.
            for entry in entries.values():
                if entry["name"] == patch["name"]:
                    raise ValueError(f"Attribute name '{patch['name']}' is not unique.")

            entries[nextID] = patch
            nextAttributeID -= 1
