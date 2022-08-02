from integrity import Hook

with Hook.at("load"):
    scoreboard players set @a other.test 0