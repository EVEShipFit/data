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

Download the latest EVE FSD from [their website](https://developers.eveonline.com/resource/resources).

Now run the tool:

```bash
python -m convert <path to fsd folder>
```

This will take a while to generate the protobuf files, but they will be outputed in the `dist` folder.

### SDE based on EVE client information

The convert script also supports loading the information from data taken from the latest EVE client.
In general, this is more up-to-date than the published SDE.
The downside is, that it requires Python2 on Windows in order to extract.

How it works:
- It downloads several `.pyd` files (which are actually DLLs, so this only works on Windows) from the installer.
- It downloads `.fsdbinary` files from the installer.
- It loads the `.pyd` files in a Python2 context. These files contain information how to load the `.fsdbinary` files.
- It exports the result as `.json` files in the `json/` folder.

Use the `download_sde/download_loaders.py` to download the files, and `download_sde/execute_loaders.py` to convert them to JSON.

Now convert them with:

```bash
python -m convert <path to json>
```

## Patches

To process data easier, and keep data small, a few things are changed in the Protobuf variant of the SDE:

- Type entries are matched to a GroupID, which is matched to a Category.
  This makes finding all types of a certain category (like: all skills) time consuming.
  As such, `CategoryID` is added to every Type entry, which is the same as the category of the group it is in.
- `domain` and `func` are strings, which is slow to process.
  As those fields are actually enums, they are changed into an integer.
  Oddly enough, `operation` is already an integer (and is an enum too).

Additionally, the EVE data has some quirks, and the EVE client tends to do some things internally.
Fixing up these things in the dogma-engine makes for a rather complicated flow, which is hard to maintain.

Instead, in the [patches](./patches/) folder there are several patches which are applied on top of the SDE, to mostly fix up these quirks and internal calculations.
These patches are all documented individually.

Although some patches fix quirks, most of them simply ensure that all clients of the dogma-engine use the same definition of the same word.
As example, calculating the `shieldBoostRate` without any of these patches is not complicated, but requires knowledge of how that value comes to be.
By pushing this into the dogma data, it means that all clients can just use `shieldBoostRate`, and all see the same value.
The complicated part of how it is built-up is already done.
One could argue that this is mis-using the dogma data and dogma-engine, but it cannot be denied it is an effective way to get the job done.

As the dogma data cannot handle all situations (and this is why some are handled by EVE client internally), there are a few additions to the dogma data:

- A `modifierInfo` with `LocationRequiredSkillModifier` or `OwnerRequiredSkillModifier` can have their `skillTypeID` set to `-1`.
  This can be used on effects defined by skills, and they cause the effect to be applied for any location / owner that has that skill as required skill.

NOTE: patches might create new attributes or effects.
New attributes and effects always have a negative ID, to quickly identify that they are not part of the original SDE.
The order of these attributes can change between builds; so use their name to find their ID.
As you should with any other attribute or effect.
