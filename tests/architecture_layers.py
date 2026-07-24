from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import yaml


@dataclass(frozen=True, slots=True)
class ArchitectureLayer:
    name: str
    paths: tuple[Path, ...]
    modules: frozenset[str]
    may_depend_on: frozenset[str]


def load_layers(root: Path) -> dict[str, ArchitectureLayer]:
    raw_config = yaml.safe_load((root / "architecture" / "layers.yaml").read_text())
    raw_layers = raw_config["layers"]
    layers: dict[str, ArchitectureLayer] = {}
    for raw_layer in raw_layers:
        name = raw_layer["name"]
        layers[name] = ArchitectureLayer(
            name=name,
            paths=tuple(root / path for path in raw_layer["paths"]),
            modules=frozenset(raw_layer["modules"]),
            may_depend_on=frozenset(raw_layer["may_depend_on"]),
        )
    return layers


def forbidden_modules(
    layers: dict[str, ArchitectureLayer],
    layer_name: str,
) -> tuple[str, ...]:
    layer = layers[layer_name]
    implementation_modules = tuple(
        sorted(module for configured_layer in layers.values() for module in configured_layer.modules)
    )
    allowed_modules = layer.modules | layer.may_depend_on
    return tuple(module for module in implementation_modules if module not in allowed_modules)


def package_paths(root: Path) -> tuple[Path, ...]:
    pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    packages = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    return tuple(root / package for package in packages if (root / package).exists())
