"""Architecture guard tests.

Enforces structural constraints that prevent architectural drift.
Run with: pytest tests/test_architecture.py -v
"""

from __future__ import annotations

import ast
from pathlib import Path

from tests.architecture_layers import forbidden_modules, load_layers, package_paths

# Project root
ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "core"
INTERFACES = CORE / "interfaces"
EVENTS = CORE / "events"
LAYERS = load_layers(ROOT)
RUNTIME_DIRS = list(LAYERS["runtime"].paths)
KNOWLEDGE_DIRS = list(LAYERS["knowledge"].paths)
ASSET_DIRS = list(LAYERS["assets"].paths)
APPLICATION_DIRS = list(LAYERS["applications"].paths)
LAYER_DIRS = RUNTIME_DIRS + KNOWLEDGE_DIRS + ASSET_DIRS
IMPLEMENTATION_MODULES = tuple(
    sorted(module for layer in LAYERS.values() for module in layer.modules)
)
RUNTIME_FORBIDDEN_MODULES = forbidden_modules(LAYERS, "runtime")
KNOWLEDGE_FORBIDDEN_MODULES = forbidden_modules(LAYERS, "knowledge")
ASSET_FORBIDDEN_MODULES = forbidden_modules(LAYERS, "assets")
PACKAGE_PATHS = package_paths(ROOT)
UNLAYERED_PACKAGE_PATHS = {CORE}


def _python_files(directory: Path) -> list[Path]:
    """Return all .py files in a directory, excluding __pycache__."""
    if not directory.exists():
        return []
    if directory.is_file():
        return [directory] if directory.suffix == ".py" else []
    return [p for p in directory.rglob("*.py") if "__pycache__" not in str(p)]


def _parse_imports(filepath: Path) -> list[str]:
    """Extract import module names from a Python file."""
    try:
        tree = ast.parse(filepath.read_text())
    except SyntaxError:
        return []

    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
    return modules


def _imports_from(module_list: list[str], target: str) -> bool:
    """Check if any import starts with the target module."""
    return any(m == target or m.startswith(target + ".") for m in module_list)


def _base_event_names(tree: ast.AST) -> set[str]:
    names = {"BaseEvent"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "core.events.base":
            for alias in node.names:
                if alias.name == "BaseEvent":
                    names.add(alias.asname or alias.name)
    return names


def _inherits_base_event(node: ast.ClassDef, base_event_names: set[str]) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in base_event_names:
            return True
        if isinstance(base, ast.Attribute) and base.attr == "BaseEvent":
            return True
    return False


class TestLayerConfig:
    def test_required_layers_are_declared(self) -> None:
        assert {"runtime", "knowledge", "assets", "applications"} <= set(LAYERS)

    def test_layer_paths_exist(self) -> None:
        missing = [
            str(path.relative_to(ROOT))
            for layer in LAYERS.values()
            for path in layer.paths
            if not path.exists()
        ]
        assert not missing, f"Layer config references missing paths: {missing}"

    def test_layer_modules_are_unique(self) -> None:
        modules = [module for layer in LAYERS.values() for module in layer.modules]
        assert len(modules) == len(set(modules)), f"Duplicate layer modules: {modules}"

    def test_first_party_implementation_files_belong_to_exactly_one_layer(self) -> None:
        layer_paths = [path for layer in LAYERS.values() for path in layer.paths]
        violations: list[str] = []
        for package_path in PACKAGE_PATHS:
            if package_path in UNLAYERED_PACKAGE_PATHS:
                continue
            for source_file in _python_files(package_path):
                owners = [path for path in layer_paths if source_file == path or path in source_file.parents]
                if len(owners) != 1:
                    violations.append(str(source_file.relative_to(ROOT)))
        assert not violations, f"Files must belong to exactly one architecture layer: {violations}"


class TestDependencyDirection:
    """Enforce Runtime → Knowledge → Assets → core/interfaces dependency direction."""

    def test_core_does_not_import_from_runtime(self) -> None:
        violations: list[str] = []
        for f in _python_files(CORE):
            imports = _parse_imports(f)
            if _imports_from(imports, "runtime"):
                violations.append(str(f.relative_to(ROOT)))
        assert not violations, f"core/ imports from runtime/: {violations}"

    def test_core_does_not_import_from_knowledge(self) -> None:
        violations: list[str] = []
        for f in _python_files(CORE):
            imports = _parse_imports(f)
            for mod in IMPLEMENTATION_MODULES:
                if _imports_from(imports, mod):
                    violations.append(f"{f.relative_to(ROOT)} → {mod}")
        assert not violations, f"core/ imports from implementation layers: {violations}"

    def test_core_does_not_import_from_applications(self) -> None:
        violations: list[str] = []
        for f in _python_files(CORE):
            imports = _parse_imports(f)
            if _imports_from(imports, "applications"):
                violations.append(str(f.relative_to(ROOT)))
        assert not violations, f"core/ imports from applications/: {violations}"

    def test_runtime_does_not_import_from_knowledge_assets_or_applications(self) -> None:
        violations: list[str] = []
        for d in RUNTIME_DIRS:
            for f in _python_files(d):
                imports = _parse_imports(f)
                for mod in RUNTIME_FORBIDDEN_MODULES:
                    if _imports_from(imports, mod):
                        violations.append(f"{f.relative_to(ROOT)} → {mod}")
        assert not violations, f"Runtime layer imports forbidden modules: {violations}"

    def test_knowledge_does_not_import_from_runtime(self) -> None:
        violations: list[str] = []
        for d in KNOWLEDGE_DIRS:
            for f in _python_files(d):
                imports = _parse_imports(f)
                for mod in KNOWLEDGE_FORBIDDEN_MODULES:
                    if _imports_from(imports, mod):
                        violations.append(f"{f.relative_to(ROOT)} → {mod}")
        assert not violations, f"Knowledge layer imports forbidden modules: {violations}"

    def test_assets_do_not_import_from_runtime_knowledge_or_applications(self) -> None:
        violations: list[str] = []
        for d in ASSET_DIRS:
            for f in _python_files(d):
                imports = _parse_imports(f)
                for mod in ASSET_FORBIDDEN_MODULES:
                    if _imports_from(imports, mod):
                        violations.append(f"{f.relative_to(ROOT)} → {mod}")
        assert not violations, f"Assets layer imports forbidden modules: {violations}"


class TestPortsOnly:
    """Enforce that core/interfaces/ contains only Protocol definitions."""

    def test_no_concrete_classes_in_interfaces(self) -> None:
        """core/interfaces/ should not contain concrete implementations."""
        violations: list[str] = []
        for f in _python_files(INTERFACES):
            if f.name == "__init__.py":
                continue
            try:
                tree = ast.parse(f.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's not a Protocol
                    is_protocol = any(
                        (isinstance(b, ast.Name) and b.id == "Protocol")
                        or (isinstance(b, ast.Attribute) and b.attr == "Protocol")
                        for b in node.bases
                    )
                    if not is_protocol and not node.name.startswith("Null"):
                        violations.append(f"{f.relative_to(ROOT)}:{node.lineno} class {node.name}")
        assert not violations, f"Non-Protocol classes in core/interfaces/: {violations}"


class TestEventOwnership:
    """Enforce that all event definitions live in core/events/."""

    def test_events_defined_only_in_core_events(self) -> None:
        violations: list[str] = []
        for d in APPLICATION_DIRS + LAYER_DIRS:
            for f in _python_files(d):
                try:
                    tree = ast.parse(f.read_text())
                except SyntaxError:
                    continue
                base_event_names = _base_event_names(tree)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef) and _inherits_base_event(node, base_event_names):
                        violations.append(f"{f.relative_to(ROOT)}:{node.lineno} class {node.name}")
        assert not violations, f"Event classes outside core/events/: {violations}"


class TestFrozenDataclasses:
    """Enforce that domain models use frozen dataclasses."""

    def test_core_models_are_frozen(self) -> None:
        violations: list[str] = []
        for f in _python_files(CORE / "models"):
            if f.name == "__init__.py":
                continue
            try:
                tree = ast.parse(f.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check for @dataclass decorator
                    has_dataclass = any(
                        (isinstance(d, ast.Name) and d.id == "dataclass")
                        or (isinstance(d, ast.Attribute) and d.attr == "dataclass")
                        for d in node.decorator_list
                    )
                    if has_dataclass:
                        # Check for frozen=True in decorator keywords
                        for d in node.decorator_list:
                            if isinstance(d, ast.Call):
                                for kw in d.keywords:
                                    if kw.arg == "frozen" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                        break
                                else:
                                    continue
                                break
                        else:
                            # Check if it has slots=True and frozen=True
                            for d in node.decorator_list:
                                if isinstance(d, ast.Call):
                                    has_slots = any(
                                        kw.arg == "slots" and isinstance(kw.value, ast.Constant) and kw.value.value is True
                                        for kw in d.keywords
                                    )
                                    has_frozen = any(
                                        kw.arg == "frozen" and isinstance(kw.value, ast.Constant) and kw.value.value is True
                                        for kw in d.keywords
                                    )
                                    if not (has_slots and has_frozen):
                                        violations.append(f"{f.relative_to(ROOT)}:{node.lineno} class {node.name}")
        assert not violations, f"Non-frozen dataclasses in core/models/: {violations}"


class TestNoBusinessLogicInCore:
    """Enforce that core/ contains only types, interfaces, and events."""

    def test_no_concrete_implementations_in_core(self) -> None:
        """core/ should not contain concrete implementations (except null_objects and exempted files)."""
        exempted = {"null_objects.py", "__init__.py", "ids.py", "exceptions.py"}
        violations: list[str] = []
        for f in _python_files(CORE):
            if f.name in exempted or "assets" in str(f) or "events" in str(f):
                continue
            if "interfaces" in str(f) or "models" in str(f):
                continue
            # Check for classes that implement interfaces
            try:
                tree = ast.parse(f.read_text())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if class inherits from any interface
                    for base in node.bases:
                        base_name = base.id if isinstance(base, ast.Name) else ""
                        if base_name and not base_name.startswith("_") and base_name != "Exception":
                            violations.append(f"{f.relative_to(ROOT)}:{node.lineno} class {node.name}({base_name})")
        assert not violations, f"Concrete implementations in core/: {violations}"
