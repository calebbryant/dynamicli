# dynamicli
Dynamically build commandline interfaces for classes and functions

#### Use
See the demo.py file for an idea of how to use.

#### Example output:
```
# python3 demo.py
usage: demo.py [-h] {example_method} ...

optional arguments:
  -h, --help        show this help message and exit

ExampleClass:
  This is the ExampleClass docstring

  {example_method}
    example_method  This is the example_method docstring

# python3 demo.py example_method --help
usage: demo.py example_method [-h] [--arg1 ARG1]

optional arguments:
  -h, --help   show this help message and exit
  --arg1 ARG1  Type: str (Default: ExampleDefault)

# python3 demo.py example_method --arg1 "This is a demo"
This is a demo```
