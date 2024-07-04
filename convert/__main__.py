import os
import sys

from .conversion import (
    dogma_attributes,
    dogma_effects,
    groups,
    market_groups,
    types,
    type_dogma,
)


if len(sys.argv) < 2:
    print("Usage: python3 convert.py <path/to/eve-sde/fsd>")
    exit(1)

path = sys.argv[1]

os.makedirs("dist/sde", exist_ok=True)
os.makedirs("dist/sde_json", exist_ok=True)

groups.convert(path)
market_groups.convert(path)
ships = types.convert(path)
type_dogma.convert(path, ships)
dogma_attributes.convert(path)
dogma_effects.convert(path)
