from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from typing import Dict, List
from beet import Context
from beet.core.utils import required_field
from bolt import Runtime
from mecha import AstChildren, AstNode, AstRoot, MutatingReducer, rule

from .api import Integrity


def beet_default(ctx: Context):
    ctx.inject(Hook)


@dataclass
class Hook:
    ctx: Context = field(repr=False)
    api: Integrity = field(init=False, repr=False)
    runtime: Runtime = field(init=False, repr=False)
    commands: Dict[str, List[AstNode]] = field(default_factory=dict)

    def __post_init__(self):
        self.api = self.ctx.inject(Integrity)
        self.runtime = self.api._runtime
        mc = self.api._mc
        mc.steps.insert(
            mc.steps.index(self.runtime.evaluate) + 1, HookResolver(api=self)
        )

    def create(self, name: str):
        node = AstHookLocation(name=name)
        self.runtime.commands.append(node)

    @contextmanager
    def at(self, name: str):
        with self.runtime.scope() as commands:
            yield
        self.commands.setdefault(name, []).extend(commands)


@dataclass(frozen=True)
class AstHookLocation(AstNode):
    name: str = required_field()


@dataclass
class HookResolver(MutatingReducer):
    api: Hook = required_field()

    @rule(AstRoot)
    def root(self, node: AstRoot):
        if not any(isinstance(child, AstHookLocation) for child in node):
            return node
        commands = []
        for child in node:
            if isinstance(child, AstHookLocation):
                hook_commands = self.api.commands.get(child.name, ())
                child_node = self.invoke(AstRoot(commands=AstChildren(hook_commands)))
                commands.extend(child_node)
            else:
                commands.append(child)
        return replace(node, commands=AstChildren(commands))
