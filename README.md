# thf-climate
Observing the microclimate of Tempelhofer Feld


## Development

### Dependencies

Ruff is used for linting and formatting. Pytest is used for testing.

```bash
pip install -r requirements-dev.txt
```

You can install the vscode extension for ruff to get linting and formatting on save [here](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### Authentication

You need to authenticate with GEE to run the code. This is done with the `gee_auth.py` script.

```bash
python thf_climate/gee/gee_auth.py
```
