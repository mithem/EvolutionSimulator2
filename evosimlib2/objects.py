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
                action = creature.act()
                if action == "die":
                    print("died")
                    self.creatures[species].pop(0)

    def update_food_count(self, iteration, callback):
        self.food_count = callback(iteration, self.initial_food)


class Creature:
    def __init__(self, **kwargs):
        self.properties = utils.creatures.get_creature_properties(kwargs)

    def reset_energy(self):
        self.properties["energy"] = 100

    def act(self):
        self.__age__ += self.__age_increments__
        if self.__age__ > self.__death_age__:
            return "die"


class Trait:
    def __init__(self, name, **effects):
        self.name = name
        self.effects = utils.traits.parse_traits(dict(effects))
