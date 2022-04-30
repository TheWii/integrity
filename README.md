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
`bolt`.

```yaml
require:
    - bolt
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

- Components

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
