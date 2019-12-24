def parse_traits(args):
    traits = {}
    if "speed" in args:
        traits["speed"] = args["speed"]
    if "sense" in args:
        traits["sense"] = args["sense"]
    if "size" in args:
        traits["size"] = args["sense"]
    return traits
