## Setup Instructions

### Prerequisites

- Python 3.9+

### Installation

1. **OPTIONAL: Generate requirements from pyproject.toml**
   ```bash
   make requirements
   ```

2. **Set up a virtual environment**
   ```bash
   make prepare-venv
   ```

### Running the Application

**Local Development**
```bash
make run-local
```

## Development Workflow

### Adding New Dependencies

1. Add the dependency to `pyproject.toml` under the `dependencies` section
2. Run `make requirements` to update requirements.txt
3. Run `make prepare-venv` to update your virtual environment

### Creating New Components

1. Add new pages in `ui/pages/`

## Makefile Commands

The project includes a Makefile with useful commands:

- `make help`: Display available commands
- `make clean`: Clean temporary files and directories
- `make requirements`: Generate requirements.txt from pyproject.toml
- `make prepare-venv`: Set up a virtual environment with dependencies
- `make run-local`: Run the Streamlit application locally
