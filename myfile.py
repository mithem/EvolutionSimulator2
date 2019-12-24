from evosimlib2.imports import *

CONFIG = {
    "World": {
        "initial_food": 100,
        "food_function": utils.functions.base,
        "initial": {
            "n_Cat": 2,
            "n_Mouse": 2}
    },
    "Creatures": {
        "Cat": {
            "reproduction_chance": 0.1,
            "death_chance": 0.1,
            "speed": 1
        },
        "Mouse": {
            "reproduction_chance": 0.1,
            "death_chance": 0.1,
            "speed": 1
        }
    },
    "iterations": 12
}


class Cat(Creature):
    pass


class Mouse(Creature):
    def __init__(self, **kwargs):
        Creature.initialize(self, **kwargs)
        print("mouse born.")