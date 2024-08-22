# EOLib

[![PyPI - Version](https://img.shields.io/pypi/v/eolib.svg)](https://pypi.org/project/eolib)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eolib.svg)](https://pypi.org/project/eolib)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Cirras_eolib-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Cirras_eolib-python)
[![Lint](https://github.com/Cirras/eolib-python/actions/workflows/lint.yml/badge.svg?event=push)](https://github.com/Cirras/eolib-python/actions/workflows/lint.yml)

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

| Command                     | Description                                            |
| --------------------------- | ------------------------------------------------------ |
| `hatch build`               | Build package                                          |
| `hatch clean`               | Remove build artifacts                                 |
| `hatch run test`            | Run unit tests with coverage                           |
| `hatch run lint:format`     | Format source files using `black`                      |
| `hatch run lint:style`      | Check formatting using `black`                         |
| `hatch run lint:typing`     | Check typing using `mypy`                              |
| `hatch run lint:all`        | Check formatting using `black` and typing using `mypy` |
| `hatch run docs:build`      | Build documentation using `mkdocs`                     |
| `hatch run docs:serve`      | Build and serve documentation using `mkdocs`           |
| `hatch run docs:deploy`     | Build and deploy documentation using `mkdocs` & `mike` |
| `hatch run release:prepare` | Prepare and tag a new release                          |