from evosimlib2 import utils
from evosimlib2.utils import creatures
import pytest


def test_get_creature_properties():
    goal = {'species': 'Coder',
            'name': 'Santa',
            'reproduction_chance': 0.1,
            'death_chance': 0.1,
            'speed': 1,
            'death_age': 120,
            'age_increments': 0.1,
            'energy': 0.1
            }
    result = utils.creatures.get_creature_properties(
        species="Coder", name="Santa", energy=0.1, death_age=120)
    print(result)
    assert result == goal
