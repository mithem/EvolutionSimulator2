"""usage:
CONFIG = {
    "World": {
        "initial_food": 1000,
        "initial": {
            "n_Cat": 100,
            "n_Dog": 100
        },
        "food_function": functions.base
    },
    "Creatures": {
        "Cat": {
            "age_increments": 1,
            "energy": 10,
            "reproduction_chance": 0.12,
            "life_efficiency": 1
        }
    },
    "iterations": 1000
}
…
python3 -m evosim2 myfile.py
"""
from evosimlib2.objects import *
from evosimlib2.utils.errors import *
import inspect


def parse_config(config, classes):
    class_names = []
    errors = []
    for i in classes:
        class_names.append(i.__name__)
    for key in config:
        if key != "World" and key != "Creatures" and key != "iterations":
            errors.append(ConfigError(
                "'" + key + "' isn't a supported config property"))
        if key == "World":
            for i in config[key]:
                # check for unsupported keys -> ConfigError
                if i != "initial_food" and i != "food_function" and i != "initial":
                    errors.append(ConfigError(
                        "'" + i + "' isn't a supported config property of config['World']"))
                # check if some keys in config > world > intial don't match to the classes -> ConfigError
                if i == "initial":
                    strings = []
                    for j in classes:
                        strings.append("n_" + str(j.__name__))
                    for k in config["World"]["initial"]:
                        if not k in strings:
                            errors.append(ConfigError(
                                "class '" + k[2:] + "' not found"))
                # if config > world > initial_food isn't int or float, raise PropertyError
                if i == "initial_food" and (type(config["World"]["initial_food"]) != int and type(config["World"]["initial_food"]) != float):
                    raise PropertyError(  # should exit
                        "invalid type for config > world > initial_food")
        if key == "Creatures":
            property_list = ["species", "name", "reproduction_chance", "death_chance", "speed",
                             "death_age", "age_increments", "energy", "age", "life_efficiency", "eat_efficiency"]
            for c in config["Creatures"]:
                if not c in class_names:
                    errors.append(ConfigError("class '" + c + "' not found"))
                for p in config["Creatures"][c]:
                    if not p in property_list:
                        errors.append(PropertyError(
                            "'" + p + "' is not a valid property for creature '" + c + "'"))
                    if type(config["Creatures"][c][p]) != int and type(config["Creatures"][c][p]) != float:
                        raise PropertyError(
                            "invalid type for config > " + c + " > " + p)
    return errors


def get_creature_properties(**kwargs):
    properties = {}
    properties["species"] = kwargs.get("species", "creature-general")
    properties["name"] = kwargs.get("name", "MyCreature")
    properties["reproduction_chance"] = kwargs.get("reproduction_chance", 0.1)
    properties["death_chance"] = kwargs.get("death_chance", 0.1)
    properties["speed"] = kwargs.get("speed", 1)
    properties["death_age"] = kwargs.get("death_age", 80)
    properties["age_increments"] = kwargs.get("age_increments", 1)
    properties["energy"] = kwargs.get("energy", 10)
    properties["age"] = kwargs.get("start_age", 0)
    properties["life_efficiency"] = kwargs.get("life_efficiency", 1)
    properties["eat_efficiency"] = kwargs.get("eat_efficiency", 40)
    return properties


def get_classes(module):
    return [
        member[1]
        for member in inspect.getmembers(
            module,
            lambda x: is_child_class(x, module)
        )
    ]


def is_child_class(obj, module):
    if not inspect.isclass(obj):
        return False
    if obj == Creature or obj == World:
        return False
    if not obj.__module__.startswith(module.__name__):
        return False
    if issubclass(obj, Creature):
        return True
    return False
