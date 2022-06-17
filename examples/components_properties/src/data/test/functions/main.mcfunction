from integrity import Component
from nbtlib import Compound

creeper = Component("creeper")
pig = Component("pig")

creeper.data["entity_id"] = "minecraft:creeper"
pig.data["entity_id"] = "minecraft:pig"

# shorthand for setting data
creeper["hostile"] = True
pig["hostile"] = False

say creeper.data
say pig.data

# shorthand for getting data
say creeper.data["entity_id"]
say creeper["entity_id"]


# component methods will always have
# the component reference as first parameter
@pig.method
def summon(entity):
  summon entity["entity_id"] ~ ~ ~

creeper.setmethod("summon", summon)

creeper.summon()
pig.summon()

@creeper.method("tp_all")
@pig.method("tp_all")
@pig.method("other_tp_all")
def tp_all_entities(entity, x, y, z):
  tp @e[type=entity["entity_id"]] x y z


creeper.tp_all(40, 63, -10)
pig.tp_all(0, 100, 0)
pig.other_tp_all(5, 20, 7)