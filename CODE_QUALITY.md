# Code Quality Scripts

This document outlines the linting and formatting scripts for the project.

## Frontend (React Native/TypeScript)

### Linting (ESLint)
```bash
npm run lint          # Check for linting errors
npm run lint:fix      # Auto-fix linting errors
```

### Formatting (Prettier)
```bash
npm run format        # Format all files
npm run format:check  # Check formatting without changing files
```

### Type Checking
```bash
npm run typecheck     # Run TypeScript compiler checks
```

### Run All Checks
```bash
npm run check         # Run typecheck, lint, and format:check
```

## Backend (Python/FastAPI)

### Formatting (Black)
```bash
cd backend
black app/           # Format all Python files
black --check app/   # Check formatting without changes
```

### Linting (Ruff)
```bash
cd backend
ruff check app/      # Check for linting errors
ruff check --fix app/  # Auto-fix linting errors
```

### Type Checking (MyPy)
```bash
cd backend
mypy app/            # Run type checks
```

### Install Dev Dependencies
```bash
cd backend
pip install -r requirements-dev.txt
```

## Pre-commit Recommendations

Consider adding these checks to your CI/CD pipeline or as pre-commit hooks:

### Frontend
- `npm run check` before committing

### Backend
- `black --check app/`
- `ruff check app/`
- `mypy app/`

## Editor Integration

### VS Code

Install these extensions:
- ESLint
- Prettier - Code formatter
- Python (includes Black, Ruff, MyPy support)

Add to `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true
}
```
