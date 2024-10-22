# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Incorrect (de)serialization of data structures containing both `<dummy>` and `<field>` elements.'
  (Only `ChestCloseServerPacket` was impacted.)
- Sanitize strings within chunked sections of protocol data structures.
  - Generated code now sets `EoWriter.string_sanitization_mode` during serialization.
  - For more information, see
    [Chunked Reading: Sanitization](https://github.com/Cirras/eo-protocol/blob/master/docs/chunks.md#sanitization).

## [1.1.1] - 2024-08-22

### Changed

- The package is now [PEP 561](https://peps.python.org/pep-0561/) compatible, exposing type
  information for usage in type checkers like
  [mypy](https://mypy.readthedocs.io/en/stable/index.html).

## [1.1.0] - 2023-12-19

### Added

- `WalkPlayerServerPacket.direction` field.

### Changed

- Remove trailing break from `ArenaSpecServerPacket`.
- Remove trailing break from `ArenaAcceptServerPacket`.
- Deprecate `WalkPlayerServerPacket.Direction` field.

## [1.0.0] - 2023-11-07

### Added

- Support for EO data structures:
  - Client packets
  - Server packets
  - Endless Map Files (EMF)
  - Endless Item Files (EIF)
  - Endless NPC Files (ENF)
  - Endless Spell Files (ESF)
  - Endless Class Files (ECF)
- Utilities:
  - Data reader
  - Data writer
  - Number encoding
  - String encoding
  - Data encryption
  - Packet sequencer

[Unreleased]: https://github.com/cirras/eolib-python/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/cirras/eolib-python/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/cirras/eolib-python/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/cirras/eolib-python/releases/tag/v1.0.0