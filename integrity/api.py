from dataclasses import dataclass
from functools import cached_property

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