#!/usr/bin/env python3

import inspect
import sys
from argparse import ArgumentParser


class DynamiCLI:
    """ DynamiCLI v0.1
    Author: Caleb Bryant
    Dynamically generates commandline interfaces for classes and functions
    - Variable types and defaults in argument help output
    - Documentation for each function as provided in the initial docstring like so
    - Can accept functions, classes, or a list of functions
    """

    def __init__(self, obj=None, help_msg: str = None):
        self.parser = ArgumentParser()
        self.obj = obj
        self._is_list = False
        if self.obj is not None:
            self.generate_cli(help_msg=help_msg)
            self.parse_args()

    def generate_cli(self, help_msg: str = None):
        help_msg = self.obj.__doc__ if help_msg is None else help_msg
        name = self._get_name(self.obj)
        subparser = self.parser.add_subparsers(
            title=name, description=help_msg)
        if inspect.isclass(self.obj):
            self.obj = self.obj()
        for method in self._get_methods():
            method_help = method.__doc__.strip(
            ) if method.__doc__ is not None else "Undocumented method for {}".format(
                name)
            argument_parser = subparser.add_parser(
                method.__name__, help=method_help)
            self._add_arguments(method, argument_parser)

    def parse_args(self):
        args = vars(self.parser.parse_args())
        self.execute(args)

    def execute(self, args):
        if len(sys.argv) > 1:
            method_name = sys.argv[1]
        else:
            self.parser.print_help()
            sys.exit()
        if self._get_name(self.obj) == method_name:
            method = self.obj
        elif self._is_list is True:
            for method in self.obj:
                if self._get_name(method) == method_name:
                    method = method
                    break
        elif hasattr(self.obj, method_name):
            method = getattr(self.obj, method_name)
        elif method_name in globals():
            method = eval(cmd_name)
        else:
            # Not sure what exception to use, so TypeError it is
            raise TypeError("Unable to locate function {}".format(method_name))

        res = method(**args)
        if res is not None:
            print(res)

    def _get_name(self, obj):
        """ Just setting this to a reusable function
        instead of using both conditionals 
        """
        if isinstance(obj, list):
            return "List of functions"
        if hasattr(obj, "__name__"):
            return obj.__name__
        return obj.__class__.__name__

    def _add_arguments(self, method, parser):
        doc_str = method.__doc__
        for arg_name, arg_data in inspect.signature(method).parameters.items():
            opts = {"help": ""}
            if arg_data.annotation is not inspect.Parameter.empty:
                opts["type"] = eval(arg_data.annotation.__name__)
                opts["help"] = "Type: {}".format(arg_data.annotation.__name__)
            if arg_data.default is not inspect.Parameter.empty:
                opts["help"] += " (Default: {})".format(str(arg_data.default))
            parser.add_argument("--{}".format(arg_name), **opts)

    def _get_methods(self):
        if self._is_callable(self.obj):
            yield self.obj
        elif isinstance(self.obj, list):
            self._is_list = True
            for func in self.obj:
                if self._is_callable(func):
                    yield func
        for method_name, method in inspect.getmembers(
                self.obj, predicate=inspect.ismethod):
            if not method_name.startswith("_"):
                yield getattr(self.obj, method_name)

    def _is_callable(self, method):
        return (inspect.isfunction(method) or inspect.ismethod(method))
