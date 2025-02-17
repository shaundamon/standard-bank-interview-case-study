# Multi-Modal Image Retrieval System Backend

## Overview

This Django-based backend system provides an API for retrieving images based on text descriptions using the CLIP model.

## Project Structure

```bash
backend/
├── config/
│ └── settings/
├── api/
├── ml/
└── manage.py
```

## Setup

1. Create virtual environment:

```bash
pip install -r requirements.txt
```

2. Get a Hugging Face API token from https://huggingface.co/settings/tokens

4. Create .env file:

```bash
cp .env.example .env
```

- add your tokens and other env variables

```env
   HUGGINGFACE_API_TOKEN=your_token_here
```

4. Run migrations:

```bash
python manage.py migrate
```

## Development

- Run development server: `python manage.py runserver`
- Run tests: `pytest`

## Documentation

- API documentation available at `/api/docs/`
- ML model documentation in `ml/README.md`


## Testing

### Running Tests

1. Install test dependencies:
```bash
pip install pytest pytest-django pytest-cov
```

2. Run all tests:
```bash
python -m pytest
```

3. Run specific test files:
```bash
# Run embedding store tests
pytest api/tests/ml/test_embeddings.py

# Run CLIP model tests
pytest api/tests/ml/test_clip.py

# Run API endpoint tests
pytest api/tests/api/test_search.py
```

4. Run tests with coverage:
```bash
pytest --cov=api --cov=ml --cov-report=term-missing
```

### Test Structure

- `tests/ml/`: ML model tests
  - `test_embeddings.py`: Tests for embedding storage and retrieval
  - `test_clip.py`: Tests for CLIP model text/image encoding
- `tests/api/`: API endpoint tests
  - `test_search.py`: Tests for image search endpoints

### Writing Tests

Example test structure:
```python
@pytest.fixture
def your_fixture():
    """Fixture description."""
    # Setup code
    yield resource
    # Cleanup code

def test_your_feature(your_fixture):
    """Test description."""
    # Test implementation
    assert expected == actual
```

### Test Coverage

Key areas covered by tests:
- Embedding store operations
- CLIP model text and image encoding
- API endpoint functionality
