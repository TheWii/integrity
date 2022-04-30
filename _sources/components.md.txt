
# Components

When developing a data pack with `bolt`, it's possible to
define several nested resources (such as functions and tags)
in a single bolt script. However, as the data pack grows in size,
working with all of these resources can get pretty cumbersome,
since most of the time we would be dealing with absolute and
relative paths. That being said, `integrity` provides an elegant
way of working with nested resources: through components.

## Component

A `Component` object is a container of nested resources, but it can
also hold data and bolt functions. To create a component, simply
import and call the `Component` factory method:

```python
from integrity import Component

my_component = Component("demo")
```

The `Component` factory can be used in various ways depending
on how we want our components to be handled.

The simplest method is by providing a unique name as first
parameter. In the example above, `my_component` is called
`demo`. Named components are children of the bolt module
they were created on. When we start defining the resources
of `my_component`, the output structure will be similar to this:

```yaml
namespace:
    - module.mcfunction
    - module:
        - components:
            - demo:
                - function_1.mcfunction
                - function_2.mcfunction
```

Note that the name `demo` becomes a folder under the
`module/components` directory. Because of that,
**a component's name needs to be unique in the module scope.**

The `Component` factory also lets us create a component without
specifying a name (i.e without any parameter):

```python
other_component = Component()
```

In this case, `other_component` is known as a module-level component.
By including it in our previous example, the updated file structure
would look like this:

```yaml
namespace:
    - module.mcfunction
    - module:
        - component:
            - function_1.mcfunction
            - function_2.mcfunction
        - components:
            - demo:
                - function_1.mcfunction
                - function_2.mcfunction
```

Module-level components are generated in the `module/component` directory,
being directly associated with its parent module.

> **Obs:** Each module can only have a single module-level component.

Alternatively, we can also create components at specific locations
by specifying a `path` parameter when using the `Component` factory:

```python
# here:module

# relative paths
my_component = Component(path=./my_component)

# absolute paths
another_component = Component(path=there:another_component)

# project root using generate_path helper function
root = Component(path=generate_path(""))
```

All of these components combined would generate the following structure:

```yaml
here:
    - module.mcfunction
    - function_1.mcfunction
    - function_2.mcfunction
    - my_component:
        - function_1.mcfunction
        - function_2.mcfunction
there:
    - another_component:
        - function_1.mcfunction
        - function_2.mcfunction
```

This way, we're in full control of the generated structure. However,
this method requires extra caution, since **two components can't**
**exist under the same path and it's easier to overwrite existing files.**  

Now that we have a `Component` object in hands, we can start defining
its properties through the API.

### API
#### Component.on

> `Component.on(event_name: str, path: str = None, tags: Iterable[str] = [])`

Registers a new function listener to the event `event_name`. If the parameter
`path` is not specified, a unique path is generated using `Component.path`.
If the parameter `tags` is specified, the registered function is added to
all function tags.

Returns the registered [resource location](https://minecraft.fandom.com/wiki/Resource_location). The returned value can be used to define a nested
function.

```python
# namespace:main

from integrity import Component

clock = Component("golden_clock")

init_path = clock.on("init")
function init_path:
    say "On clock init"

function clock.on("tick", tags=["minecraft:tick"]):
    say "On clock tick"

function clock.on("second"):
    say "On clock second"

function clock.on("second"):
    say "Also on clock second"

function clock.on("second", ./path_to/second):
    say "On clock second but explicit path"

clock.on("second", demo:existing_function/do_stuff)
```

This example would generate the following functions:

```yaml
namespace:
    - main.mcfunction
    - main:
        - components:
            - golden_clock:
                - init.mcfunction
                - tick.mcfunction
                - second.mcfunction
                - second_1.mcfunction
    - path_to:
        - second.mcfunction
demo:
    - existing_function:
        - do_stuff.mcfunction
```

Events will also generate function tags if more than one
listener is registered:

```yaml
namespace:
    - main:
        - components:
            - golden_clock:
                - second.json
minecraft:
    - tick.json
```

Since both the `init` and `tick` events only have a single function
listener, function tags are not generated and the events will refer
to their listener paths directly when using `Component.run`.

#### Component.run

> `Component.run(event_name: str)`

Generates a `function` command that calls the event `event_name`.
If the event only has a single function listener, the listener
is called directly, otherwise the event function tag is called instead.
If the provided `event_name` argument is prefixed by `#`, the event
function tag is forcedly called.

The command is generated regardless if the function/function tag exists.

```python
# demo:main

from integrity import Component

core = Component(path=./core)

core.on("tick", ./tick)

core.run("tick")
# function demo:tick

core.on("stuff") # generates path for us
core.on("stuff")

core.run("stuff")
# function #demo:core/stuff

core.run("next") # not implemented
# function demo:core/next

core.run("#prepare")
# function #demo:core/prepare
```

#### Component.data

A `dict` object to store anything that might belong to a specific component.
All components are created with an empty `data` field.

```python
from integrity import Component

player = Component("player")
player.data["entity_id"] = "minecraft:player"

pig = Component("pig")
player.data["entity_id"] = "minecraft:pig"

player.data # { "entity_id": "minecraft:player" }
pig.data # { "entity_id": "minecraft:pig" }
```

#### Component.path

> `Component.path(relative: str, tag: bool = False)`

Generates a [resource location](https://minecraft.fandom.com/wiki/Resource_location)
based on the component root path and the provided `relative` argument.
If `tag` is `True`, a tag resource location (prefixed by `#`) is
generated instead.

```python
from integrity import Component

player = Component(path=./player)

predicate player.path("is_sneaking") {
    ...
}

if predicate player.path("is_sneaking") say Hi!

loot spawn ~ ~ ~ loot player.path("weapons/iron_sword")
```
