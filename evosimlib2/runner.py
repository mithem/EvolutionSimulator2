import fileloghelper
import matplotlib.pyplot as plt
from fileloghelper import Logger

import evosimlib2.utils
from evosimlib2.objects import *
from evosimlib2.utils import functions
from evosimlib2.utils.errors import *


def main(module, config, logger=None, verbose=False):
    if logger == None:
        logger = Logger("runner_main.log", "runner.py > main", autosave=True)
    else:
        logger.set_context("runner.py > main()")
    classes = utils.get_classes(module)
    errors = utils.parse_config(config, classes)
    for i in errors:
        if type(i) == ConfigError:
            logger.error("ConfigError: " + str(i), True)
        elif type(i) == PropertyError:
            logger.warning("PropertyError: " + str(i), True)
    w = World(initial_food=config.get("World").get("initial_food", 100),
              food_function=config.get("World").get("food_function", functions.base))
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


def do_iterations(world, iterations, logger=None, config={}):
    if logger == None:
        logger = Logger("runner_do_iterations", "iterations", autosave=True)
    else:
        logger.set_context("iterations")
    raw_data = {}
    for species in world.creatures:
        raw_data[species] = []
    raw_data["food"] = []
    raw_data["population"] = []
    csv_lines = []
    try:
        species_count = {
            "iteration": 0,
            "food_count": world.food_count,
            "food_count_before": world.food_count_before,
            "population": 0
        }
        mystr = str("iteration, food count, food count before, population")
        for species in world.creatures:
            species_count[species] = len(species)
            mystr += ", " + species
        species_vs = fileloghelper.VarSet(species_count)
        print(mystr)
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

            species_vs.set("iteration", iteration)
            for species in world.creatures:
                species_vs.set(species, len(species))
            species_vs.set("food_count", world.food_count)
            species_vs.set("food_count_before", world.food_count_before)
            species_vs.set("population", population)
            species_vs.print_variables()

            # reduced (string) logging to csv file (i.e. for later analysis)
            #csv_lines.append(string + "\n")
    except KeyboardInterrupt:
        pass
    except KeyError:
        pass
    except Exception as e:
        raise e
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


def display_data(data):
    plt.plot(data["food"], label="food available")
    for species in data:
        if species != "food":
            plt.plot(data[species], label=species)
    plt.legend()
    plt.title("Evolution Simulator 2")
    plt.show()
