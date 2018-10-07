from dynamicli import DynamiCLI


def say_hello(name: str = "World"):
    """ This is the docstring to the 'say_hello' function
	"""
    return "Hello {}".format(name)


class ExampleClass:
    """ This is the ExampleClass docstring
	"""

    def example_method(self, arg1: str = "ExampleDefault"):
        """ This is the example_method docstring
		"""
        return arg1

    def _example_hidden_method(self):
        """ This is the _example_hidden_method docstring - 
        it will not be included in the CLI
		"""
        pass


if __name__ == '__main__':
    DynamiCLI(ExampleClass)
