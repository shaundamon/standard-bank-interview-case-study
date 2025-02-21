# Multi-Modal Image Retrieval System Backend

## Overview

This Django-based backend system provides an API for retrieving images based on text descriptions using the CLIP model.

This supports our frontend application which allows users to search for images using natural language queries.

## Project Structure

```bash
backend/
├── config/
│ └── settings/
├── api/
├── ml/
└── manage.py
```

## Server Setup

1. Install dependencies:

**_NB_**: Ensure you have activated your virtual env which you must've created and activated from here : [Main README](../README.md)

```bash
pip install -r requirements.txt
```

2. Create .env file:

```bash
cp .env.example .env
```

- add your tokens and other env variables

```env
   # Django settings
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

   # Database settings - OPTIONAL for postgres
   DB_NAME=your_db_name
   DB_USER=your_user_name
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432

   # ML Settings
   DATA_PATH=/path/to/your/data
   MODEL_NAME=openai/clip-vit-base-patch32
   EMBEDDING_DIM=512
   BATCH_SIZE=32
   TOP_K=5
   SAMPLE_SIZE=500

   # Kaggle Settings
   KAGGLE_USERNAME=your_kaggle_username # for dataset download(optional, below explains the data part)
   KAGGLE_KEY=your_kaggle_api_key

   # Hugging Face Settings
   HUGGINGFACE_API_TOKEN=your_token_here
```

## Dataset Setup

The application handles dataset storage differently based on your setup:

### Docker Setup
Data is automatically stored in a Docker volume at `/app/data`

### Local Setup
By default, data is stored in:
- Windows: `C:\Users\<username>\.imageai\data`
- Linux/Mac: `~/.imageai/data`

You can override this by setting `DATA_PATH` in your `.env` file:

```env
DATA_PATH=/custom/path/to/data
```

If you prefer to download manually instead:
- Download from [AI vs Human Generated Dataset](https://www.kaggle.com/datasets/alessandrasala79/ai-vs-human-generated-dataset/data?select=test_data_v2)
- Extract to `api/data/dataset/`
- Update your `.env`: `DATASET_PATH=api/data/dataset`


3. Run migrations:

```bash
python manage.py migrate
```

4. Run development server:
```bash
python manage.py runserver
```

## Documentation

- API documentation available at `/api/docs/`

## Testing

### Running Tests

1. Install test dependencies:
```bash
pip install pytest pytest-django pytest-cov
```

2. Run all tests:
```bash
pytest 
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

### Test Coverage

Key areas covered by tests:
- Embedding store operations
- CLIP model text and image encoding
- API endpoint functionality

