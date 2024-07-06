import os
import sys

from .conversion import (
    categories,
    dogma_attributes,
    dogma_effects,
    groups,
    market_groups,
    types,
    type_dogma,
)
from .patches import (
    dogma_attributes as patch_dogma_attributes,
    dogma_effects as patch_dogma_effects,
    type_dogma as patch_type_dogma,
)
from .patches.loader import load_patches


if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist/sde", exist_ok=True)
os.makedirs("dist/sde_json", exist_ok=True)

patches = load_patches()

data = {}
gens = []

gens.append(categories.convert(path, data))
gens.append(groups.convert(path, data))
gens.append(types.convert(path, data))
gens.append(market_groups.convert(path, data))
gens.append(dogma_attributes.convert(path, data, patches))
gens.append(dogma_effects.convert(path, data, patches))
gens.append(type_dogma.convert(path, data, patches))

# First iteration updates "data" with all the name -> ID mappings.
for gen in gens:
    next(gen)

# Patch all data.
patch_dogma_attributes.patch(data["dogmaAttributes"], patches["attributes"], data)
patch_dogma_effects.patch(data["dogmaEffects"], patches["effects"], data)
patch_type_dogma.patch(data["typeDogma"], patches["typeDogma"], data)

# Second iteration actually writes all the information.
for gen in gens:
    try:
        next(gen)
    except StopIteration:
        pass
