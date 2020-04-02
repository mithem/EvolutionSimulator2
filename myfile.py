from evosimlib2.imports import *

CONFIG = {
    "World": {
        "initial_food": 1000,
        "initial": {
            "n_Coronavirus": 100,
        },
        "food_function": functions.base
    },
    "Creatures": {
        "Coronavirus": {
            "age_increments": 1,
            "energy": 10,
            "reproduction_chance": 0.13
        }
    },
    "iterations": 1000
}


class Coronavirus(Creature):
    pass
