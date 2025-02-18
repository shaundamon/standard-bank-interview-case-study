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

## Dataset Setup

The project uses an AI vs Human Generated Image dataset from Kaggle. There are two ways to get the dataset:

### Option 1: Automatic Download (Recommended)
The application will automatically download the dataset when you start it for the first time. This is handled by the `DatasetManager` class using the Kaggle API.

1. Get your Kaggle API credentials:
   - Go to your Kaggle account settings (https://www.kaggle.com/settings)
   - Scroll to "API" section and click "Create New Token"
   - This will download a `kaggle.json` file

2. Place your Kaggle credentials:
   - On Windows: `C:\Users\<YOUR-USERNAME>\.kaggle\kaggle.json`
   - On Linux/macOS: `~/.kaggle/kaggle.json`

### Option 2: Manual Download
If you prefer to download the dataset manually:

1. Visit the dataset page: [AI vs Human Generated Dataset](https://www.kaggle.com/datasets/alessandrasala79/ai-vs-human-generated-dataset/data?select=test_data_v2)

2. Click the "Download" button (requires Kaggle account)

3. Extract the downloaded zip file

4. Place the `test_data_v2` folder contents in:
   ```
   api/data/dataset/
   ```

5. Update your `.env` file to point to the correct path:
   ```
   DATASET_PATH=api/data/dataset
   ```

**_Note_**: The dataset zip file is 10GB in size but you only need a sample of 500


## Server Setup

1. Install dependencies:

**_NB_**: Ensure you are have activated your virtual env

```bash
pip install -r requirements.txt
```

2. Get a Hugging Face API token from https://huggingface.co/settings/tokens

3. Create .env file:

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
   KAGGLE_USERNAME=your_kaggle_username # for dataset download
   KAGGLE_KEY=your_kaggle_api_key

   # Hugging Face Settings
   HUGGINGFACE_API_TOKEN=your_token_here
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Run development server:
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
