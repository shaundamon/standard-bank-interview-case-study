# WebApp for the MMIR System

## Overview

The frontend is a React-based  application built with Vite for the Multi-Modal Image Retrieval System. It provides an intuitive user interface for searching images using natural language queries.

## Prerequisites

- Node.js 16+
- npm or yarn
- Backend API running (see ../api/README.md)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Configure environment variables:
```env
VITE_API_URL=http://localhost:8000
```

## Development

Start the development server:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`

## Building for Production

1. Create production build:
```bash
npm run build
```

2. Preview production build:
```bash
npm run preview
```

## Project Structure

```bash
webapp/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── hooks/         # Custom React hooks
│   ├── utils/         # Utility functions
│   ├── types/         # TypeScript type definitions
│   └── App.tsx        # Root component
├── public/            # Static assets
└── vite.config.ts     # Vite configuration
```

## Features

- Responsive image grid layout
- Real-time search functionality
- Image preview modal
- Loading states and error handling
- Similarity score display

## Contributing

1. Create a new branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## Dependencies

- React 18
- TypeScript
- Vite
- TailwindCSS
- React Query
- Axios
- React Router
