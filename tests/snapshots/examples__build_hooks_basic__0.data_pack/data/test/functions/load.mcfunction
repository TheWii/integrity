say Loading...
execute as @a[tag=!loaded] run function test:main/nested_execute_0
scoreboard players set @a other.test 0
say Loaded.
scoreboard players reset @a *
