from dataclasses import dataclass, field
from typing import Any, Dict

from beet import Context

from .api import Integrity


@dataclass
class Components:
    ctx: Context
    components: Dict[str, "Component"] = field(default_factory=dict)
    api: Integrity = field(init=False)

    def __post_init__(self):
        self.api = self.ctx.inject(Integrity)

    def __call__(self, name: str = None):
        return self.create(name)

    def create(self, name: str = None):
        path = self.generate_path(name)
        if path in self.components:
            raise ValueError(
                f"Path '{path}' is already being used by another component."
            )
        component = Component(self, name, path)
        self.components[path] = component
        return component

    def generate_path(self, name: str = None):
        current = self.api._runtime.get_path()
        if not name:
            return f"{current}/component"
        return f"{current}/components/{name}"


@dataclass
class Component:
    ref: Components
    name: str
    root: str
    data: Dict[str, Any] = field(default_factory=dict)
    mcfunctions: Dict[str, str] = field(default_factory=dict)

    def path(self, relative: str):
        return f"{self.root}/{relative}"

    def on(self, function_name: str):
        path = self.path(function_name)
        self.mcfunctions[function_name] = path
        return path

    def run(self, function_name: str):
        if not self.mcfunctions.get(function_name):
            self.on(function_name)
        path = self.mcfunctions[function_name]
        self.ref.api._inject_command(f"function {path}")
