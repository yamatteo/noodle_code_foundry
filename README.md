# Noodle Code Foundry

A [copier](https://copier.readthedocs.io/) generator for uv-managed Python
projects. Answer a handful of questions and get a ready-to-run package, with
optional Zensical documentation, Jupyter notebook compilation, docs hosting CI and
the pauli-braun Claude Code workflow. The generated project keeps no link back
to this repository.

## Usage

```bash
uvx copier copy gh:yamatteo/noodle_code_foundry my_project
```

or, from a local clone:

```bash
uvx copier copy path/to/noodle_code_foundry my_project
```

Then:

```bash
cd my_project
git init
uv run my-project
```

## Questions

| Question | Default | What it controls |
|----------|---------|------------------|
| `project_name` | — | Human-readable name, used in the README, docs title and greeting |
| `project_slug` | derived from `project_name` | Python package name (must be a valid identifier); the distribution and script name is the slug with `-` instead of `_` |
| `description` | empty | One-line description in `pyproject.toml`, README and docs |
| `author_name` | — | Author in `pyproject.toml`, LICENSE and docs |
| `author_email` | — | Author email in `pyproject.toml` |
| `license` | `MIT` | `MIT`, `Apache-2.0` or `None` (no LICENSE file, no `license` field) |
| `copyright_year` | current year | Year in the MIT copyright notice (asked only for MIT) |
| `docs` | `false` | Adds a Zensical documentation site in `docs/`, configured by `zensical.toml` |
| `notebooks` | `false` | Adds `notebooks/`, the notebook compilation scripts and a `dev` dependency group (asked only with `docs`) |
| `docs_hosting` | `github-pages` | `github-pages`, `gitlab-pages` or `none`: which CI file deploys the docs (asked only with `docs`) |
| `pauli_braun` | `true` | Adds `.claude/settings.json` recommending the pauli-braun plugin |

## Pauli/Braun

[pauli-braun](https://github.com/yamatteo/pauli_braun) is a Claude Code plugin
for a single-thread workflow: Pauli plans and reviews, Braun builds. When
`pauli_braun` is enabled, the generated `.claude/settings.json` registers the
plugin's marketplace and enables the plugin, so Claude Code offers to install it
when you trust the project folder. Run `/pauli` to start. It does not set an
output style, so nobody is switched into Pauli mode by default. Answer `no` to
leave it out.

## Cookbook

This section contains reusable recipes and patterns for common Python
development tasks.

### Environment Variables with python-dotenv

This project uses `python-dotenv` to manage environment variables from a local
`.env` file.

#### Installation
```bash
uv add python-dotenv
```

#### Basic Usage

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
database_url = os.getenv("DATABASE_URL")
debug_mode = os.getenv("DEBUG", "False")  # with default value
```

#### Common Patterns

**1. Simple Script (Local Development)**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # finds .env automatically
SECRET = os.getenv("SECRET")
DEBUG = os.getenv("DEBUG", "False")
```

**2. Explicit Environment File Selection**
```python
from dotenv import load_dotenv, find_dotenv
import os

env = os.getenv("PYTHON_ENV", "development")
load_dotenv(find_dotenv(f".env.{env}"))
```

**3. Read-Only Parsing (No Environment Modification)**
```python
from dotenv import dotenv_values

config = dotenv_values(".env")
database_url = config.get("DATABASE_URL")
```


#### API Reference

| Function | Purpose |
|----------|---------|
| `load_dotenv()` | Load .env into `os.environ` |
| `dotenv_values()` | Parse .env to dict (no env change) |
| `find_dotenv()` | Locate .env file |
| `get_key(file, key)` | Read single key from file |
| `set_key(file, key, value)` | Update/add key in file |
| `unset_key(file, key)` | Remove key from file |

#### Best Practices

- **Security**: Never commit `.env` files to version control
- **Template**: Commit `.env.example` with required keys (no values)
- **Production**: Use platform environment variables or secret managers
- **Override**: Use `override=False` (default) to preserve system env vars
- **Validation**: Check required variables at startup and fail fast

#### .env File Format

```bash
# Database
DATABASE_URL="postgres://user:password@localhost/dbname"

# Redis
REDIS_URL="redis://localhost:6379"

# App settings
DEBUG=True
SECRET_KEY="your-secret-key"

# Variable expansion
BASE_URL="https://api.example.com"
FULL_URL="${BASE_URL}/v1"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## Support

- Create an issue on Github
- Email: yamatteo@gmail.com

---

**Note**: This README serves as both project documentation and a cookbook.