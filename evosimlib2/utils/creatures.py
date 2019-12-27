def get_creature_properties(**kwargs):
    properties = {}
    properties["species"] = kwargs.get("species", "creature-general")
    properties["name"] = kwargs.get("name", "MyCreature")
    properties["reproduction_chance"] = kwargs.get("reproduction_chance", 0.1)
    properties["death_chance"] = kwargs.get("death_chance", 0.1)
    properties["speed"] = kwargs.get("speed", 1)
    properties["death_age"] = kwargs.get("death_age", 100)
    properties["age_increments"] = kwargs.get("age_increments", 0.1)
    properties["energy"] = kwargs.get("energy", 100)
    properties["age"] = kwargs.get("start_age", 0)
    properties["life_efficiency"] = kwargs.get("life_efficiency", 1)
    properties["eat_efficiency"] = kwargs.get("eat_efficiency", 40)
    return properties
