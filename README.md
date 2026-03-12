# Stalse AI Inbox

An AI-Augmented Mini Inbox application built for the Stalse technical challenge. This project features automatic support ticket classification and priority suggestion using LLM (Gemini).

## 🚀 Overview

The system is a monorepo containing:
- **Frontend**: Next.js (App Router), TypeScript, and TailwindCSS.
- **Backend**: Python (FastAPI) with SQLite for persistence and Gemini AI integration.

## 🛠️ Tech Stack

- **Frontend**: Next.js, TypeScript, TailwindCSS (Orange/Black theme).
- **Backend**: FastAPI, SQLite, Gemini AI API.
- **DevOps**: Docker Compose

## 🏃 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.9+
- Gemini API Key

### Installation

1. Clone the repository.
2. Configure environment variables in a `.env` file (see `.env.example`).

### Running the Project

#### Using Docker
```bash
docker-compose up
```

#### Manual Start

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python seed.py # Optional: Seed initial data
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

- **Backend**: `cd backend && pytest`
- **Frontend**: `cd frontend && npm run test`

## 🏗️ Architecture

- `/frontend`: Next.js application.
- `/backend`: FastAPI application and AI services.
- `/backend/database`: SQLite database storage.

---
Built by Rafael Monteiro
