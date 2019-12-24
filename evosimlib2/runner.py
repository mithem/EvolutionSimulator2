from evosimlib2.objects import *
import inspect


def main(module, config):
    w = World(initial_food=config.get("World").get("initial_food"),
              food_function=config.get("World").get("food_function"))
    classes = get_classes(module)
    for ccllss in classes:
        w.creatures[ccllss.__name__] = []
        for i in range(config.get("World").get("initial").get("n_" + ccllss.__name__)):
            w.creatures[ccllss.__name__].append(ccllss())
    do_iterations(w, config.get("iterations"))


def do_iterations(world: World, iterations):
    for iteration in range(iterations):
        world.act(iteration)
        string = str(iteration)
        for i in world.creatures:
            string += ", " + str(len(world.creatures.get(i)))
        print(string)


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
