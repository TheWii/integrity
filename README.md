# Integrity

[![GitHub Actions](https://github.com/thewii/integrity/workflows/CI/badge.svg)](https://github.com/thewii/integrity/actions)
[![PyPI](https://img.shields.io/pypi/v/integrity.svg)](https://pypi.org/project/integrity/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/integrity.svg)](https://pypi.org/project/integrity/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Discord](https://img.shields.io/discord/900530660677156924?color=7289DA&label=discord&logo=discord&logoColor=fff)](https://discord.gg/98MdSGMm8j)

> Development facilities for the bolt environment

```python
from integrity import Component

from ./settings import settings
from ./blocks import blocks
from ./player import player

main = Component()

function main.on("main"):
    if score settings.data.activated obj matches 1:
        main.run("active")

function main.on("active"):
    as @a at @s:
        player.run("main")

function blocks.on("placed_by_player"):
    if block ~ ~ ~ stone expand:
        say Placed stone!
        player.run("placed_stone")

```

## Installation

The package can be installed with `pip`. Note, you must have
both `beet` and `mecha` installed to use this package.

```bash
$ pip install integrity
```

## Getting Started

To use this package, we must add the plugin to the `require`
section in the `beet` project file alongside with `mecha` and
`mecha.contrib.bolt`.

```yaml
require:
    - mecha.contrib.bolt
    - integrity
pipeline:
    - mecha
```

Now that we've enabled `integrity`, we can import the module
directly inside a bolt script

```python
from integrity import Component

foo = Component("foo")
```

## Features

### Components

When developing a data pack with `bolt`, it's possible to
define several nested resources (such as functions and tags)
in a single bolt script. However, as the data pack grows in size,
structuring all of these resources can get pretty cumbersome,
since most of the time you'd be working with absolute and
relative paths. That being said, `integrity` provides an elegant
way of working with nested resources: through components.

A `Component` object is a container of nested resources, but can
also hold data and bolt functions. To create a component, simply
import and call the `Component` factory method:

```python
from integrity import Component

my_component = Component("demo")
```

When creating a component, we can provide a unique name as a parameter. In this
case, `my_component` is called `demo`.

> **Note:** A component's name must be **unique in the module scope**.

With a `Component` object in hands, we can start defining its properties
through the API.

#### **Component.on(function_name: str): str**

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

#### **Component.run(function_name: str)**

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

#### **Component.data**

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

## Contributing

Contributions are welcome. Make sure to first open an issue
discussing the problem or the new feature before creating a
pull request. The project uses [`poetry`](https://python-poetry.org).

```bash
$ poetry install
```

You can run the tests with `poetry run pytest`.

```bash
$ poetry run pytest
```

The project must type-check with [`pyright`](https://github.com/microsoft/pyright).
If you're using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
extension should report diagnostics automatically. You can also install
the type-checker locally with `npm install` and run it from the command-line.

```bash
$ npm run watch
$ npm run check
```

The code follows the [`black`](https://github.com/psf/black) code style.
Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).

```bash
$ poetry run isort bolt_expressions examples tests
$ poetry run black bolt_expressions examples tests
$ poetry run black --check bolt_expressions examples tests
```

---

License - [MIT](https://github.com/rx-modules/bolt-expressions/blob/main/LICENSE)
