from evosimlib2.imports import *

CONFIG = {
    "World": {
        "initial_food": 1000,
        "initial": {
            "n_Cat": 500
        }
    },
    "Creatures": {
        "Cat": {
            "reproduction_chance": 0.275,
            "death_chance": 0.275,
            "speed": 10,
            "age_increments": 1,
            "death_age": 80
        }
    },
    "iterations": 10000
}


class Cat(Creature):
    pass
