import evosimlib2.utils as utils
import evosimlib2.utils.functions as functions
import evosimlib2.utils.traits as traits
import evosimlib2.utils.creatures as creatures
import random


class World:
    def __init__(self, initial_food=100, food_function=functions.base):
        self.creatures = {}
        self.food_count = initial_food
        self.initial_food = initial_food
        self.food_count_before = initial_food
        self.food_function = food_function

    def act(self, iteration, config):
        self.update_food_count(iteration, self.food_function)
        self.food_count = self.food_count_before
        creature_query = []
        for species in self.creatures:
            for c in self.creatures[species]:
                creature_query.append(c)
        random.shuffle(creature_query)
        for creature in creature_query:
            actions = creature.act()
            if "reproduce" in actions:
                new_creature = self.get_renewed_creature(creature, config)
                new_creature.act()
                self.creatures[creature.properties["species"]].append(
                    new_creature)
            if "die" in actions:
                self.kill_creature(creature)
            if "eat" in actions:
                if self.food_count > 0:
                    creature.eat()
                    self.food_count -= 1
                else:
                    self.kill_creature(creature)  # really?

    def get_renewed_creature(self, creature, config):
        creature.properties["age"] = config.get("Creatures", {}).get(
            creature.properties["species"]).get("age", 0)
        creature.properties["energy"] = config.get("Creatures", {}).get(
            creature.properties["species"]).get("energy", 50)
        return creature

    def kill_creature(self, obj):
        try:
            self.creatures[obj.properties.get("species")].pop(
                self.creatures[obj.properties.get("species")].index(obj))
        except IndexError:
            pass

    def update_food_count(self, iteration, callback):
        self.food_count_before = callback(x=iteration, base=self.initial_food)


class Creature:
    def __init__(self, **kwargs):
        self.properties = creatures.get_creature_properties(**kwargs)

    def reset_energy(self):
        self.properties["energy"] = 100

    def act(self):

        actions = []

        # energy
        self.properties["energy"] -= self.properties["life_efficiency"]

        # aging
        self.properties["age"] += self.properties["age_increments"]
        if self.properties["age"] > self.properties["death_age"] or self.properties["energy"] <= 0:
            actions.append("die")

        # dying
        if random.random() <= self.properties["death_chance"]:
            actions.append("die")

        # eating
        actions.append("eat")

        # reproduction
        if random.random() <= self.properties["reproduction_chance"]:
            actions.append("reproduce")

        return actions

    def eat(self):
        self.properties["energy"] += self.properties["eat_efficiency"]


class Trait:
    def __init__(self, name, **effects):
        self.name = name
        self.effects = utils.traits.parse_traits(dict(effects))
