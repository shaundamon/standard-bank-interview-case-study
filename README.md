# Multi-Modal Image Retrieval System

A case study for Standard Bank as part of their recruitment process for a **Specialist : AI Engineer** role.

This build is focused on showcasing a full end-to-end implementation of a Multi-Modal Image retrieval application.

## Features
- Text-to-image search using natural language queries
- Multiple AI model support (CLIP and BLIP2)
- RESTful API architecture
- Real-time image similarity search
- Efficient embedding storage and retrieval
- Scalable architecture 

## Project Structure
```bash
project/
├── webapp/ 
├── api/ 
│ ├── ml/ 
│ ├── api/ 
│ └── config/ 
└── docs/ 
└── notebooks/
```

## Prerequisites
- Python 3.8+
- Node.js 16+
- Docker

## Quick Start - using Docker

1. Clone the repository:

```bash
git clone https://github.com/shaundamon/standard-bank-interview-case-study.git

cd standard-bank-interview-case-study
```

2. Copy the example environment file and rename it:

```bash
cp .env.example .env
```

3. [**Optional - Only required when switching from CLIP to BLIP2 model**] Add your Hugging Face API token to the .env file (get one at https://huggingface.co/settings/tokens):

4. Build and start the containers:

```bash
docker-compose up --build
```

5. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs/

## Quick Start - locally

1. Clone the repository:

```bash
git clone https://github.com/shaundamon/standard-bank-interview-case-study.git

cd standard-bank-interview-case-study
```

2. Set up the backend (see [Backend Setup](api/README.md))

3. Set up the frontend (see [Frontend Setup](webapp/README.md))

## Architecture Overview

### Backend
- Django REST Framework for API endpoints
- CLIP and BLIP2 models for image-text similarity
- Efficient embedding storage system
- Scalable image processing pipeline

### Frontend
- React with Vite for fast development
- TypeScript for type safety
- TailwindCSS for styling
- React Query for state management

## API Documentation
Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`


---
