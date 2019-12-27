from evosimlib2.imports import *

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
            "reproduction_chance": 0.12
        },
        "Dog": {
            "age_increments": 1,
            "energy": 10,
            "reproduction_chance": 0.115
        }
    },
    "iterations": 1150
}


class Cat(Creature):
    pass


class Dog(Creature):
    pass
