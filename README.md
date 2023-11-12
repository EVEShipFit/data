# Data used by EVEShip.fit

To have the best experience possible, we convert the EVE SDE dataset into a format that is as small as possible and readable as fast as possible.

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
