# Alcatel LinkZone SDK

## Documentation

[https://linkzone.readthedocs.io/](https://linkzone.readthedocs.io/)

## Installation

### For development

- First create a virtual environment

``` bash
python -m venv .venv
```

- Activate the virtual environment

``` bash
source .venv/bin/activate
```

- Install pip-tools

``` bash
pip install pip-tools
```

- Resolve project dependencies

``` bash
pip-compile -o requirements.txt pyproject.toml
```

- Optional dev dependencies

``` bash
pip-compile --extra dev -o dev-requirements.txt pyproject.toml
```

- Optional doc dependencies
pip-compile --extra docs -o docs-requirements.txt pyproject.toml

- Install dependencies

``` bash
pip install -r requirements.txt
```

``` bash
pip install -r dev-requirements.txt
```

```bash
pip install -r docs-requirements.txt
```

## Created by

[@JimScope](https://twitter.com/JimScope)
