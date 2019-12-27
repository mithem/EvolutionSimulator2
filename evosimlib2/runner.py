from evosimlib2.objects import *
from fileloghelper import Logger
import matplotlib.pyplot as plt
import inspect


def main(module, config, logger=Logger(filename="runner_main.txt"), verbose=False):
    logger.set_context("runner.py > main()")
    w = World(initial_food=config.get("World").get("initial_food", 100),
              food_function=config.get("World").get("food_function", functions.base))
    classes = get_classes(module)
    for ccllss in classes:
        w.creatures[ccllss.__name__] = []
        n_of_class = config.get("World", {}).get(
            "initial", {}).get("n_" + ccllss.__name__, 1)
        for i in range(n_of_class):
            c = ccllss(name=ccllss.__name__, species=ccllss.__name__, reproduction_chance=config.get("Creatures", {}).get(ccllss.__name__, {}).get("reproduction_chance", 0.1), death_chance=config.get("Creatures", {}).get(ccllss.__name__, {}).get("death_chance", 0.1), speed=config.get("Creatures", {}).get(
                ccllss.__name__, {}).get("speed", 1), death_age=config.get("Creatures", {}).get(ccllss.__name__, {}).get("death_age", 100), age_increments=config.get("Creatures", {}).get(ccllss.__name__, {}).get("age_increments", 0.1), energy=config.get("Creatures", {}).get(ccllss.__name__, {}).get("energy", 100))
            w.creatures[ccllss.__name__].append(c)
        logger.debug("Added " + str(n_of_class) +
                     " instances of " + ccllss.__name__ + " to the world", verbose)
    data = do_iterations(w, config.get("iterations"), logger, config)
    logger.save()
    display_data(data)


def do_iterations(world, iterations, logger=Logger(filename="runner_doIterations.txt"), config={}):
    logger.set_context("iterations")
    raw_data = {}
    for species in world.creatures:
        raw_data[species] = []
    raw_data["food"] = []
    raw_data["population"] = []
    csv_lines = []
    try:
        for iteration in range(iterations):
            world.act(iteration, config)

            # array logging for matplotlib
            population = 0
            for species in world.creatures:
                n_of_animals_in_species = len(world.creatures[species])
                raw_data[species].append(n_of_animals_in_species)
                population += n_of_animals_in_species
            raw_data["food"].append(world.food_count_before)
            raw_data["population"].append(population)

            # string for logging & console output
            string = str(iteration + 1)
            for species in world.creatures:
                string += ", " + str(len(world.creatures.get(species)))
            string += ", " + str(world.food_count) + ", " + \
                str(world.food_count_before) + ", " + str(population)
            logger.debug(string, True)

            # reduced (string) logging to csv file (i.e. for later analysis)
            csv_lines.append(string + "\n")
    except KeyboardInterrupt:
        pass
    finally:
        logger.save()
        f = open("raw_data.csv", "w")
        header = "timestamp, "
        for i in raw_data:
            header += i + ", "
        header = header[:-2]
        f.write(header + "\n")
        f.writelines(csv_lines)
        f.close()
        return raw_data


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


def display_data(data):
    plt.plot(data["food"], label="food available")
    for species in data:
        if species != "food":
            plt.plot(data[species], label=species)
    plt.legend()
    plt.title("Evolution Simulator 2")
    plt.show()
