# Noodle Code Foundry

A Python project template and cookbook for sharing reusable recipes, patterns, and best practices across projects.

## Project Structure

```
short_name/
├─ .env
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
├─ README.md
└─ src/
   └─ short_name/
      ├─ __init__.py
      └─ main.py
```

## Cookbook

This section contains reusable recipes and patterns for common Python development tasks.

### Environment Variables with python-dotenv

This project uses `python-dotenv` to manage environment variables from a local `.env` file.

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

### Start a new project

To start a new project run:
```bash
uv init --package --vcs git --no-pin-python <short_name>
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue on Github
- Email: yamatteo@gmail.com

---

**Note**: This README serves as both project documentation and a cookbook.