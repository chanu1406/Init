# Init

A daily, structured learning application for CS undergraduates focused on systems fundamentals, DevOps basics, and practical system design thinking.

## Project Structure

```
├── app/                    # Expo Router screens (file-based routing)
├── components/             # Reusable UI components
├── services/               # API client, Supabase client
├── store/                  # Zustand stores for local/session state
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript type definitions
├── lib/                    # Utility functions
├── constants/              # App-wide constants and config
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── core/           # Config, dependencies, security
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic (grading, scheduling)
│   │   ├── models/         # Pydantic models for DB entities
│   │   └── schemas/        # Request/Response schemas
└── assets/                 # Images, fonts, static files
```

## Tech Stack

### Frontend
- React Native (Expo)
- TypeScript
- Expo Router (navigation)
- NativeWind (styling)
- Zustand (local state)
- TanStack Query (server state)

### Backend
- Python FastAPI
- Pydantic
- Supabase PostgreSQL
- OpenAI API (GPT-4o)

## Getting Started

### Frontend

```bash
# Install dependencies
npm install

# Start development server
npm start
```

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:
- `EXPO_PUBLIC_SUPABASE_URL`: Your Supabase project URL
- `EXPO_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anon key
- `EXPO_PUBLIC_API_URL`: Backend API URL

For the backend, copy `backend/.env.example` to `backend/.env`.

## Core Concepts

- **Tracks**: High-level learning paths (e.g., systems-101, devops-basics)
- **Units**: Ordered sections within a track
- **Drills**: Atomic learning actions (explain, debug, quiz)
- **Mastery**: Numeric representation of understanding (0-5)

## License

Private - All rights reserved.
