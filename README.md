# Tempelhof Climate

## Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Architecture](#project-architecture)
4. [Data Sources](#data-sources)
5. [Installation](#installation)
   - [Normal Installation](#normal-installation)
   - [Docker Installation](#docker-installation)
6. [Authentication](#authentication)
7. [Linting and Formatting](#linting-and-formatting)
8. [Sponsors](#sponsors)
9. [License](#license)

## Project Overview
**Tempelhof Climate Change Analysis** is a collaborative project by the CODE University software engineering group aimed at observing climate changes occurring at Tempelhof Feld by analyzing satellite images.

## Prerequisites
- Python 3.x
- Git

## Project Architecture
To-do

## Data Sources
- [Google Earth Engine](https://earthengine.google.com)

## Installation

### Normal Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codeuniversity/thf-climate.git
   ```
2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```
3. Copy the env.sample file to .env and set the required variables:
   ```bash
   cp env.sample .env
   ```

### Docker Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codeuniversity/thf-climate.git
   ```
2. Build the Docker image:
   ```bash
   docker build --tag thf-climate .
   ```
3. Run the Docker Container:
   ```bash
   docker run --publish 8000:8000 thf-climate
   ```

## Running the API

Run the API locally using:

```bash
fastapi dev src/main.py
```

Serving at: http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs

## Authentication

You need to authenticate with GEE to run the code. This is done with the `auth.py` script.

```bash
python src/gee/auth.py
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

## Linting and Formatting

[Ruff](https://docs.astral.sh/ruff/) is used for linting and formatting.

You can install the vscode extension for ruff to get linting and formatting on save [here](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## Sponsors
- **CODE University**
- **Google Earth Engine**

## License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See the LICENSE file for more details.
