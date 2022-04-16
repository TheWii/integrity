from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Dict, Iterable, List

from beet import Context, FunctionTag
from beet.core.utils import required_field
from mecha import AstChildren, AstCommand, AstResourceLocation, MutatingReducer, rule

from .api import Integrity


@dataclass
class Components:
    ctx: Context = field(repr=False)
    components: Dict[str, "Component"] = field(default_factory=dict)
    api: Integrity = field(init=False, repr=False)

    def __post_init__(self):
        self.api = self.ctx.inject(Integrity)
        self.api._mc.transform.extend(ComponentTransformer(api=self))

    def create(self, name: str = None, path: str = None):
        if path is None:
            path = self.generate_path(name)
        if path in self.components:
            raise ValueError(
                f"Path '{path}' is already being used by another component."
            )
        component = Component(self, path)
        self.components[path] = component
        return component

    __call__ = create

    def generate_path(self, name: str = None):
        current = self.api._runtime.get_path()
        if name is None:
            return f"{current}/component"
        return f"{current}/components/{name}"

    def generate_tags(self):
        for component in self.components.values():
            for event_name, event in component.events.items():
                if not event["tag"]:
                    continue
                path = component.path(event_name)
                self.ctx.data.function_tags.merge(
                    {path: FunctionTag({"values": event["values"]})}
                )


@dataclass
class Component:
    ref: Components = field(repr=False)
    root: str
    data: Dict[str, Any] = field(default_factory=dict)
    methods: Dict[str, Callable] = field(default_factory=dict)
    events: Dict[str, List[str]] = field(default_factory=dict)

    def _get_or_create_event(self, event_name: str):
        event = self.events.setdefault(event_name, {})
        event.setdefault("values", [])
        event.setdefault("tag", False)
        return event

    def path(self, relative: str, tag: bool = False):
        prefix = "#" if tag else ""
        if self.root.endswith(":"):
            return prefix + self.root + relative
        return f"{prefix}{self.root}/{relative}"

    def on(self, event_name: str, path: str = None, tags: Iterable[str] = ()):
        event = self._get_or_create_event(event_name)
        values = event["values"]
        if path is None:
            path = self.path(event_name)
            if i := len(values):
                path = f"{path}_{i}"
        if not path in values:
            values.append(path)
            if not event["tag"] and len(values) > 1:
                event["tag"] = True
        for tag in tags:
            self.ref.api._inject_raw(
                f'merge function_tag {tag} {{"values":["{path}"]}}'
            )
        return path

    def run(self, event_name: str):
        force_tag = False
        if event_name.startswith("#"):
            event_name = event_name[1:]
            force_tag = True
        event = self._get_or_create_event(event_name)
        if force_tag:
            event["tag"] = True
        location = AstEventResourceLocation(component=self.root, path=event_name)
        node = AstCommand(identifier="function:name", arguments=AstChildren([location]))
        self.ref.api._inject_command(node)

    def setmethod(self, name: str, function: Callable[["Component"], Any]):
        self.methods[name] = partial(function, self)

    def __getattr__(self, key: str):
        return self.methods[key]

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value


@dataclass(frozen=True)
class AstEventResourceLocation(AstResourceLocation):
    component: str = required_field()


@dataclass
class ComponentTransformer(MutatingReducer):
    api: Components = required_field()

    @rule(AstEventResourceLocation)
    def event_resource_location(self, node: AstEventResourceLocation):
        component = self.api.components.get(node.component)
        if not component:
            raise ValueError(f"Component '{node.component}' does not exist.'")
        event = component._get_or_create_event(node.path)
        values = event["values"]
        is_tag = event["tag"]
        if len(values) == 1:
            full_path = values[0]
        else:
            full_path = component.path(node.path)
        namespace, _, path = full_path.partition(":")
        return AstResourceLocation(namespace=namespace, path=path, is_tag=is_tag)
