from integrity import Component

main = Component(path=./main)


function main.on("single"):
  say Single function call

main.run("single")



function main.on("many"):
  say first listener

function main.on("many"):
  say second listener

main.run("many")




main.run("run_single_before_definition")

function main.on("run_single_before_definition"):
  say Still a single function call.



function main.on("many_but_defined_after_run"):
  say First listener.

main.run("many_but_defined_after_run")

function main.on("many_but_defined_after_run"):
  say Second listener.



main.run("not_defined_but_run_as_single")

main.run("#not_defined_but_run_as_many")



function main.on("single_but_forced_to_be_a_tag"):
  say Single listener.

main.run("#single_but_forced_to_be_a_tag")



function main.on("single_with_explicit_path", ./foo):
  say Single listener defined with explicit path.

main.run("single_with_explicit_path")



function main.on("many_across_namespaces", demo1:foo):
  say Across namespace on demo1

function main.on("many_across_namespaces", demo2:foo):
  say Across namespace on demo2

main.run("many_across_namespaces")



main.data["rainbow_colors"] = ("red", "orange", "yellow", "green", "blue", "indigo", "violet")

for color in main.data.rainbow_colors:
  function main.on("rainbow", main.path(f"color/{color}")):
    say f"I like {color}"

main.run("rainbow")