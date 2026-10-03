# SpLegalMart

A full-stack legal services platform scaffold with:

- FastAPI backend at `backend/app`
- React + Vite frontend at `frontend`
- Landing page, booking form, admin dashboard shell
- In-memory seed data for services and bookings
- Admin login credentials in `app/memory/test_credentials.md`

## Stack

- Backend: FastAPI, Pydantic, JWT, in-memory storage
- Frontend: React, Vite, Tailwind-ready CSS, Framer Motion
- Branding: navy / gold / paper palette inspired by the PRD

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

API runs at: http://localhost:8001

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

App runs at: http://localhost:5173

## Admin credentials

See `app/memory/test_credentials.md`:

- Email: admin@splegalmart.com
- Password: admin123

## Notes

This repository contains a working starter implementation aligned with the PRD, with dummy data and real API routes to support the booking and admin flows. The app is designed to be extended with MongoDB, real authentication, and production-grade admin features.
