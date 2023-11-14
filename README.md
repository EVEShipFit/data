# Data used by EVEShip.fit

To have the best experience possible with EVEShip.fit, we convert the EVE SDE dataset into a format that is as small as possible and readable as fast as possible.

For this we use Google's Protobuf, and we strip out a lot of fields we don't actually need.

## Protobuf definition

In this folder is a tool (`convert.py`), which converts the YAML files from the SDE into Protobuf (v2) binary files.

In `esf.proto` is the Protobuf definition.
This is exported to Python and Javascript with the following commands:

```bash
protoc --python_out=. esf.proto
web/node_modules/.bin/pbjs -t static-module -w es6 -o esf_pb2.js esf.proto --no-create --no-encode --no-verify --no-convert --no-delimited --no-typeurl --no-beautify --no-comments --no-service
```

## Converting

Download the latest EVE SDE from [their website](https://developers.eveonline.com/resource/resources).

Now run the tool:

```bash
python convert.py <path to fsd folder inside the sde>
```

This will take a while to generate the protobuf files, but they will be outputed in the `dist` folder.

## Patches

The EVE SDE has some quirks, that are easiest fixed in the conversion.

- TypeID entries are matched to a GroupID, which is matched to a Category.
  This makes finding all types of a certain category (like: all skills) time consuming.
  As such, `CategoryID` is added to every TypeID entry, which is the same as the category of the group it is in.
- A few attributes are added to every hull, which are calculated by the `dogma-engine`.
  They carry negative IDs, to make it more visible they are calculated by the `dogma-engine`, and are not part of the EVE SDE.
  - `-1`: `alignTime` - seconds needed to align for warp.
  - `-2`: `scanStrength` - there are four types of scan-strengths; this is given the highest value of those four.
  - `-3`: `cpuUsed` - how much CPU is in use.
  - `-4`: `powerUsed` - how much Power Grid is in use.
  - `-5`: `cpuUnused` - how much CPU is left unused.
  - `-6`: `powerUnused` - how much Power Grid is left unused.
  - `-7`: `velocityBoost` - how much (in percent) the velocity will be boosted (for AB / MWD calculations).
- The effect `online` is in the category `active` (for internal EVE reasons).
  But this confuses the `dogma-engine` in calculating the possible states a module can have.
  As such, the category is changed to `online`.
- `domain` and `func` are strings, which is slow to process.
  As those fields are actually enums, they are changed into an integer.
  Oddly enough, `operation` is already an integer (and is an enum too).
- Afterburners and Microwarpdrive have no active effect modifier in the SDE (as they are handled specially internally in EVE).
  To address this, the `moduleBonusAfterburner` and `moduleBonusMicrowarpdrive` get assigned extra modifiers:
  - A modifier with the operation `add`, with on the left side `massAddition` of the item and on the right side `mass` of the ship.
  - A modifier with the operation `postPercent`, with on the left side `signatureRadiusBonus` of the item and on the right side `signatureRadius` of the ship.
  - A few complicated modifier to change the `maxVelocity`.
    In normal math terms: `maxVelocity *= item.speedFactor * item.speedBoostFactor / ship.mass`.
    The issue is that this combines attributes from the item and ship, which is normally never done like this.
    As a solution, two things are changed:
    - Two modifiers are added which result attribute `-7` on the ship to be the `item.speedFactor * item.speedBoostFactor` part.
    - A new effect (`-1`: `applyVelocityBoost`) is added to all ships, which add two modifiers to do the rest: `/ ship.mass` and applying as `postPercent` to `maxVelocity`.
