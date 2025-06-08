# COPCLASS Project

This is a Python project for COPCLASS.

## Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `src/`: Source code directory
- `tests/`: Test files directory
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## Development

To run tests:
```bash
pytest
```

To format code:
```bash
black .
```

To check code style:
```bash
flake8
``` 