---
title: Home
---
# env-exec

[![PyPI - Version](https://img.shields.io/pypi/v/env-exec.svg)](https://pypi.org/project/env-exec)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/env-exec.svg)](https://pypi.org/project/env-exec)

## Overview

The `env-exec` library is a versatile Python utility designed for managing computational environments and containers, as well as executing code within them. It aims to simplify the process of setting up, utilizing, and tearing down different kinds of environments, including but not limited to Conda environments. 

## Installation

```bash
pip install env-exec
```

## Usage

Create an ephemeral Conda environment with dependencies installed.

```python
with CondaEnv(dependencies=['python']) as env:
    # Execute a command in the environment
    env.exec('python -V') 
# The environment is automatically cleaned up after exiting the context manager
```

Capture the output of executed commands.

```python
with CondaEnv(dependencies=['python']) as env:
    output = env.exec('python -V', capture_output=True)
    print(output.stdout) # Python 3.8.5
```

Give the environment a name to prevent it from being deleted. If the environment already exists, it will be reused.

```python
with CondaEnv('my-env', dependencies=['python']) as env:
    env.exec('python -V')

CondaEnv('my-env').exists # True
```

Error if dependencies are missing from env.

```python
# Raises MissingDependencyError
with CondaEnv('my-env', dependencies=['python', 'numpy']) as env:
    pass
```

Install dependencies if they are missing.

```python
with CondaEnv('my-env', dependencies=['python', 'numpy'], install_missing=True) as env:
    env.exec('python -c "import numpy"')
```

## Features

### Environment Management

- **Automated Setup**: Create new computational environments programmatically.
- **Dependency Management**: Specify and manage dependencies for each environment.
- **Dynamic Names**: Generate random environment names or specify them manually.
  
### Command Execution

- **Run Code**: Execute code blocks, shell commands, or scripts within the environment.
- **Capture Output**: Option to capture the output of executed commands.

### Error Handling

- **Custom Exceptions**: Well-defined exceptions for handling environment-specific issues.
  
### Extensible Design

- **Pluggable Backends**: Easily extend the library to support other environment managers or container systems.
  
### Cleanup

- **Context Manager**: Use as a context manager to ensure proper resource cleanup.

## Dependencies

- Python 3.7 or higher
- Conda installed and accessible via the command line (if using `CondaEnv`)

## Extending for Other Managers

You can also extend the library to create your own environment managers. Just inherit from the `Env` class and implement the required methods.

## Error Handling

The library raises custom exceptions for more explicit error handling. These include:

- `ExecError`: Raised if an error occurs while executing a command in the environment.
- `MissingDependencyError`: Raised if missing dependencies are found and not installed.

## Contributing

Contributions are welcome! If you have a feature request, bug report, or wish to contribute code, please feel free to open an issue or a pull request.

## License

The code in this project is licensed under MIT. Please see the accompanying LICENSE file for details.
