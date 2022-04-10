from integrity import Component

# Top-level component located at main/component
toplevel = Component()

function toplevel.on("init"):
  say Toplevel init



# Child component located at main/components/foo
child_foo = Component("foo")

function child_foo.on("init"):
  say Foo init



# Child component located at main/components/bar
child_bar = Component("bar")

# Enforce function path "./bar_init" to child_bar's "init"
function child_bar.on("init", ./bar_init):
  say Bar init



# Create component at test:path/to/abc
abc = Component(path=./path/to/abc)

function abc.on("init"):
  say Abc init



function ./existing_main:
  say Not directly associated with a component

# Register "./existing_main" to abc's "main"
abc.on("main", ./existing_main)
# Also register "./existing_main" to bar's "main"
child_bar.on("main", ./existing_main)

abc.run("main")
child_bar.run("main")



# Make a collection of components
components = [
  toplevel,
  child_foo,
  child_bar,
  abc
]


# Project root
root = Component(path=generate_path(""))

function root.on("init"):
  say Root init. Init all sub-components
  for comp in components:
    comp.run("init")