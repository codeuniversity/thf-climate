# thf-climate
Observing the microclimate of Tempelhofer Feld


## Development

### Setup

Create a virtual environment and install the dependencies.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Copy the env.sample file to .env and set the required variables.
```bash
cp env.sample .env
```

### Linting and Formatting


[Ruff](https://docs.astral.sh/ruff/) is used for linting and formatting.

You can install the vscode extension for ruff to get linting and formatting on save [here](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

### Authentication

You need to authenticate with GEE to run the code. This is done with the `auth.py` script.

```bash
python thf_climate/gee/auth.py
```

If you have authenticated before, you will most likely find your credentials in the following files. Add those credentials to your .env, then run the command above.

Linux/ Mac:
```
$HOME/.config/earthengine/credentials
 ```

 Windows:
```
%UserProfile%\.config\earthengine\credentials
```
