from integrity import Hook

function ./load:
    say Loading...
    Hook.create("load")
    say Loaded.
    Hook.create("loaded")

with Hook.at("load"):
    as @a[tag=!loaded]:
        say Loading player
        Hook.create("player:load")
        tag @s add loaded

with Hook.at("player:load"):
    scoreboard players set @s example.score 123
    align xyz positioned ~.5 ~.5 ~.5 expand:
        Hook.create("player:load/centered")
    tag @s remove abc

with Hook.at("player:load/centered"):
    setblock ~ ~ ~ stone

with Hook.at("player:load/centered"):
    particle flame ~ ~ ~ 0 0 0 0.1 1 force


with Hook.at("loaded"):
    scoreboard players reset @a *