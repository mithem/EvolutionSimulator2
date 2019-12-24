import evosimlib2.utils as utils
import evosimlib2.utils.functions as functions
import evosimlib2.utils.traits as traits


class World:
    def __init__(self, initial_food=100, food_function=functions.base):
        self.creatures = {}
        self.food_count = initial_food
        self.initial_food = initial_food
        self.food_function = food_function

    def act(self, iteration=0):
        self.update_food_count(iteration, self.food_function)
        for species in self.creatures:
            for creature in self.creatures.get(species):
                creature.act()

    def update_food_count(self, iteration, callback):
        self.food_count = callback(iteration, self.initial_food)


class Creature:
    def __init__(self, species="creature-general", name="MyCreature", reproduction_chance=0.1, death_chance=0.1, speed=0.1):
        self.__species__ = species
        self.__name__ = name
        self.__reproduction_chance__ = reproduction_chance
        self.__death_chance__ = death_chance
        self.__speed__ = speed
        self.reset_energy()

    def reset_energy(self):
        self.__energy__ = 100

    def act(self):
        pass


class Trait:
    def __init__(self, name, **effects):
        self.name = name
        self.effects = utils.traits.parse_traits(dict(effects))
