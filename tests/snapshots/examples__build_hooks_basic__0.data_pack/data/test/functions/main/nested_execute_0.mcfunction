say Loading player
scoreboard players set @s example.score 123
execute align xyz positioned ~0.5 ~0.5 ~0.5 run setblock ~ ~ ~ stone
execute align xyz positioned ~0.5 ~0.5 ~0.5 run particle flame ~ ~ ~ 0 0 0 0.1 1 force
tag @s remove abc
tag @s add loaded
