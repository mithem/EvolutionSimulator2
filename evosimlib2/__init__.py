import argparse
import evosimlib2.utils
import evosimlib2.runner
import os
import importlib
from evosimlib2.objects import Trait
from fileloghelper import Logger

__version__ = "0.0.1"


def parse_args():
    parser = argparse.ArgumentParser(
        description="A high-level Library for creating simulations of basic ecosystems without graphics", usage="python3 -m evosim2 [options] [file]")
    parser.add_argument("file", nargs="?",
                        help="File explaining the simulation")
    parser.add_argument("-v", "--version",
                        action="version", version=__version__)
    args = parser.parse_args()
    return vars(args)


def get_module(file_name):
    module_name = get_module_name(file_name)
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_module_name(file_name):
    try:
        module_name = file_name.replace(os.sep, ".").replace(".py", "")
    except AttributeError:
        module_name = input(
            "Path to the file with the source code for the simulation> ")
        module_name = get_module_name(module_name)
    return module_name


def main():
    args = parse_args()
    module = get_module(args.get("file"))
    config = getattr(module, "CONFIG")
    runner.main(module, config)
