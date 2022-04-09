from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Dict

from beet import Context
from mecha import Mecha
from mecha.contrib.bolt import Runtime


@dataclass
class Integrity:
    ctx: Context

    @cached_property
    def _mc(self):
        return self.ctx.inject(Mecha)

    @cached_property
    def _runtime(self):
        return self.ctx.inject(Runtime)

    def _inject_command(self, cmd: str):
        self._runtime.commands.append(self._mc.parse(cmd, using="command"))

    def get_path(self, name: str):
        current = self._runtime.get_path()
        return f"{current}/components/{name}"

    def component(self, name: str):
        return Component(self, name, self.get_path(name))


@dataclass
class Component:
    ref: Integrity
    name: str
    root: str
    data: Dict[str, Any] = field(default_factory=dict)
    methods: Dict[str, str] = field(default_factory=dict)

    def path(self, relative: str):
        return f"{self.root}/{relative}"

    def on(self, method: str):
        path = self.path(method)
        self.methods[method] = path
        return path

    def run(self, method: str):
        if not self.methods.get(method):
            self.on(method)
        path = self.methods[method]
        self.ref._inject_command(f"function {path}")
