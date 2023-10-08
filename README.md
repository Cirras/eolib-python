# EOLib

[![PyPI - Version](https://img.shields.io/pypi/v/eolib.svg)](https://pypi.org/project/eolib)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eolib.svg)](https://pypi.org/project/eolib)

A core Python library for writing applications related to Endless Online.

## Installation

```console
pip install eolib
```

## Features

Read and write the following EO data structures:

- Client packets
- Server packets
- Endless Map Files (EMF)
- Endless Item Files (EIF)
- Endless NPC Files (ENF)
- Endless Spell Files (ESF)
- Endless Class Files (ECF)

Utilities:

- Data reader
- Data writer
- Number encoding
- String encoding
- Data encryption
- Packet sequencer

## Development

### Requirements

- [Python](https://www.python.org/downloads/) 3.8+
- [Hatch](https://hatch.pypa.io/latest/install/)

### Available Commands

| Command                 | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `hatch build`           | Build package                                          |
| `hatch clean`           | Remove build artifacts                                 |
| `hatch run test`        | Run unit tests with coverage                           |
| `hatch run lint:format` | Format source files using `black`                      |
| `hatch run lint:style`  | Check formatting using `black`                         |
| `hatch run lint:typing` | Check typing using `mypy`                              |
| `hatch run lint:all`    | Check formatting using `black` and typing using `mypy` |