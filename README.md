# Data used by EVEShip.fit

To have the best experience possible with EVEShip.fit, we convert the EVE SDE dataset into a format that is as small as possible and readable as fast as possible.

For this we use Google's Protobuf, and we strip out a lot of fields we don't actually need.

## Protobuf definition

In this folder is a tool (`convert.py`), which converts the YAML files from the SDE into Protobuf (v2) binary files.

In `esf.proto` is the Protobuf definition.
This is exported to Python and Javascript with the following commands:

```bash
protoc --python_out=. esf.proto
npx pbjs -t static-module -w es6 -o esf_pb2.js esf.proto --no-create --no-encode --no-verify --no-convert --no-delimited --no-typeurl --no-beautify --no-comments --no-service
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
- Some Missile skills have no active effect modifier in the SDE (as they are handled specially internally in EVE).
  To address this, for these skill, an extra effect is applied.
  The function `OwnerRequiredSkillModifier` with a SkillID of `-1` is used to indicate the effect should be applied based on the current skill.
  Similar, `selfRof` and `droneDmgBonus` have no effects applied.
  These are changed in a similar way.
- Some missile attributes are applied to CharID, and not to the charge.
  The new effect (`-2`: `applyMissileDamage`) is added to the character, which applies `missileDamageMultiplier` to all four damage types on all charges that need `Missile Launcher Operation` skill.
- A few attributes are added to every hull, which are calculated by the `dogma-engine`.
  They carry negative IDs, to make it more visible they are calculated by the `dogma-engine`, and are not part of the EVE SDE.
  - `-1`: `alignTime` - seconds needed to align for warp.
  - `-2`: `scanStrength` - there are four types of scan-strengths; this is given the highest value of those four.
  - `-3`: `cpuUsed` - how much CPU is in use.
  - `-4`: `powerUsed` - how much Power Grid is in use.
  - `-5`: `cpuUnused` - how much CPU is left unused.
  - `-6`: `powerUnused` - how much Power Grid is left unused.
  - `-7`: `velocityBoost` - how much (in percent) the velocity will be boosted (for AB / MWD calculations).
  - `-8`: `shieldEhpMultiplier` - multiplier to convert shield HP to shield eHP.
  - `-9`: `armorEhpMultiplier` - multiplier to convert armor HP to armor eHP.
  - `-10`: `hullEhpMultiplier` - multiplier to convert hull HP to hull eHP.
  - `-11`: `shieldEhp` - shield eHP.
  - `-12`: `armorEhp` - armor eHP.
  - `-13`: `hullEhp` - hull eHP.
  - `-14`: `ehp` - total (shield + armor + hull) eHP.
  - `-15`: `passiveShieldRecharge` - passive shield recharge (in HP/s).
  - `-16`: `shieldBoostRate` - shield boost rate (in HP/s).
  - `-17`: `armorRepairRate` - armor repair rate (in HP/s).
  - `-18`: `hullRepairRate` - hull repair rate (in HP/s).
  - `-19`: `passiveShieldRechargeEhp` - passive shield recharge (in eHP/s).
  - `-20`: `shieldBoostRateEhp` - shield boost rate (in eHP/s).
  - `-21`: `armorRepairRateEhp` - armor repair rate (in eHP/s).
  - `-22`: `hullRepairRateEhp` - hull repair rate (in eHP/s).
  - `-23`: `capacitorPeakRecharge` - peak recharge of capacitor (in GJ/s).
  - `-24`: `capacitorPeakUsage` - peak usage of capacitor (in GJ/s), when all modules would activate at the same time.
  - `-25`: `capacitorPeakDelta` - delta between peak recharge and usage (in GJ/s).
  - `-26`: `capacitorPeakDeltaPercentage` - delta between peak recharge and usage in percentage against peak recharge.
  - `-27`: `capacitorDepletesIn` - if capacitor is unstable, amount of seconds till the capacitor is drained.
  - `-28`: `damageWithoutReloadDps` - the total DPS without reloading.
  - `-29`: `damageWithReloadDps` - the total DPS with reloading.
  - `-30`: `damageAlphaHp` - the damage done when all guns shoot at once.
