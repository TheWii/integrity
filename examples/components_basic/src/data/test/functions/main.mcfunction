from integrity import Component

stuff = Component("stuff")
stuff.data["message"] = "Hello World!"

function stuff.on("greet"):
  say stuff.data["message"]

stuff.run("greet")