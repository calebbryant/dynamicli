#!/usr/bin/env python3

import inspect
import sys
from argparse import ArgumentParser


class DynamiCLI:
	""" DynamiCLI v0.1
	Author: Caleb Bryant
	Dynamically generates commandlines for classes and functions
	Includes:
	- Variable types and defaults in argument help output
	- Documentation for each function as provided in the initial docstring like so
	"""
	def __init__(self, obj = None, help_msg: str = None):
		self.parser = ArgumentParser()
		self.sub_parsers = {}
		if obj is not None:
			self.generate_cli(obj, help_msg=help_msg)
			self.parse_args()

	def generate_cli(self, obj, help_msg: str = None):
		help_msg = obj.__doc__ if help_msg is None else help_msg
		name = obj.__class__.__name__ if not hasattr(obj, "__name__") else getattr(obj, "__name__")
		subparser = self.parser.add_subparsers(title=name, description=help_msg)
		if inspect.isclass(obj):
			obj = obj()
		for method in self._get_methods(obj):
			method_help = method.__doc__.strip() if method.__doc__ is not None else "Undocumented method for {}".format(name)
			argument_parser = subparser.add_parser(method.__name__, help=method_help)
			self._add_arguments(method, argument_parser)

	def parse_args(self, args: list = None):
		args = sys.argv if args is None else args
		self.parser.print_help()

	def execute(self):
		pass

	def _add_arguments(self, method, parser):
		doc_str = method.__doc__
		opts = {}
		for arg_name, arg_data in inspect.signature(method).parameters.items():
			default_val = "(Default: {}".format(arg_data.default) if type(arg_data.default).__name__ is not "type" else "No Default"
			if hasattr(default_val, '__type__'):
				default_val_type = "Type: {}".format(default_val.__type__)
			else:
				default_val_type = "Type: None Specified"
			parser.add_argument("--{}".format(arg_name), help = "{} {}".format(default_val_type, default_val))

	def _get_methods(self, obj):
		if inspect.isfunction(obj):
			yield obj
		for method_name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
			if not method_name.startswith("_"):
				yield getattr(obj, method_name)
