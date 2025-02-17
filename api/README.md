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
- Run tests: `python manage.py test`

## Documentation

- API documentation available at `/api/docs/`
- ML model documentation in `ml/README.md`
