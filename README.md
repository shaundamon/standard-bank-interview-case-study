# Multi-Modal Image Retrieval System

A case study for Standard Bank as part of their recruitment phase for a **Specialist : AI Engineer**.

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

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/shaundamon/standard-bank-interview-case-study.git

cd standard-bank-interview-case-study
```

2. Set up the backend (see [Backend Setup](api/README.md)):

3. Set up the frontend (see [Frontend Setup](webapp/README.md)):

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

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---