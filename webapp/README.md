# WebApp for the MMIR System

## Overview

The frontend is a React-based  application built with Vite for the Multi-Modal Image Retrieval System. It provides an intuitive user interface for searching images using natural language queries with an extension to cater for the disiabled people by allowing screen reader feedback and voice input queries.

This is supported by our django api backend which provides the necessary endpoints for retrieving images based on text descriptions and returns top matching neighbors.

## Prerequisites

- Node.js 16+
- npm or yarn
- Backend API running (see [Backend Setup](../api/README.md))

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Configure environment variables:
```env
VITE_API_URL=http://localhost:8000
# Optional: Supabase configuration (only if using Supabase for auth)
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key # for auth management
VITE_SUPABASE_URL=your_supabase_url
```

**Note**: For development without Supabase, you can skip setting the Supabase environment variables. The app will automatically use a mock auth functionality that accepts any email/password combination for testing purposes.

## Development

Start the development server:
```bash
npm run dev
```
The application will be available at `http://localhost:5173`

## Project Structure

```bash
webapp/
├── src/
│   ├── components/   
│   ├── pages/         
│   ├── services/   
│   ├── hooks/         
│   ├── utils/         
│   ├── types/         
│   └── App.tsx      
├── public/          
└── vite.config.ts     
```

## Features

- Responsive image grid layout
- Real-time search functionality
- Image preview modal
- Loading states and error handling
- Similarity score display

## Dependencies

- React 18
- TypeScript
- Vite
- TailwindCSS
- React Query
- Axios
- React Router
