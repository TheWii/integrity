
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

### Component.on(function_name: *str*): *str*

Creates and returns a [resource location](https://minecraft.fandom.com/wiki/Resource_location) associated with the given
`function_name` value. The returned `str` value can be used to define a nested
function:

```python
# main.mcfunction

from integrity import Component

clock = Component("golden_clock")


tick_function_path = clock.on("tick")

function tick_function_path:
    say "Clock ticks"


function clock.on("midnight"):
    say "It's midnight"


function ./tick:
    clock.run("tick")
```

This example would generate the following file structure:

```yaml
root:
    - tick.mcfunction
    - main.mcfunction
    - main:
        - components:
            - golden_clock:
                - tick.mcfunction
                - midnight.mcfunction
```

> **Note:** This structure might change in the future and/or will be
customizable.

### Component.run(function_name: *str*)

Generates a `function` command that calls the function with
the specified `function_name` value. The command is generated regardless
if the function exists.

```python

from integrity import Component

beam = Component("beam")

function beam.on("raycast"):
    unless block ~ ~ ~ air:
        beam.run("hit")
    if block ~ ~ ~ air:
        beam.run("raycast")

function beam.on("hit"):
    setblock ~ ~ ~ air destroy

function beam.on("tick"):
    if entity @s[tag=right_clicked]:
        beam.run("raycast")
    tag @s remove right_clicked


function ./tick:
    beam.run("clear") # not implemented yet
    as @a at @s:
        beam.run("tick")
```

### Component.data: *dict[str, Any]*

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

### Component.path(relative: *str*, tag: *bool* = False)
