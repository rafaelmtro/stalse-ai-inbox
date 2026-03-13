# Project: Stalse AI Inbox

**Repository:** `stalse-ai-inbox`
**Author:** Rafael Monteiro
**Version:** `v1.0.0` (First Stable Release)

An AI-Augmented Mini Inbox application built for the Stalse technical challenge, structured as a **monorepo**. The system focuses on delivering robust results without over-engineering, featuring automatic support ticket classification and response drafting via an LLM.

## Code Style

- Strict TypeScript: Absolute prohibition of `any` types; usage is considered a severe fault. This is strictly enforced via `noImplicitAny: true` in TypeScript configuration and `@typescript-eslint/no-explicit-any: error` in ESLint.
- Frontend Stack: Next.js (App Router), TypeScript, TailwindCSS, and Recharts.
- Backend Stack: Python (FastAPI), using **uv** for lightning-fast package and virtual environment management.
- Pragmatism: MVP-first approach. Focus on delivering the end-to-end flow.
- UI/UX Design: Minimalist design, "B2B DNA". The interface features:
    - High-density table-like layout for ticket management.
    - Status-based filtering.
    - Modal-driven interface for creating and viewing ticket details.
    - Interactive rows with AI-powered response drafting.
    - **Analytics Dashboard (`/dashboard`)** providing real-time metrics and category distribution charts via Recharts.
    - Strict adherence to an **Orange and Black** color palette.
- Testing: Comprehensive unit testing is required for both frontend components/utilities and backend API features/LLM logic.
- Commit Standards: Commits should follow a structured pattern (such as Conventional Commits) to improve the reading and understanding of the project's history.

## Commands

- `docker-compose up`: Boot both the Frontend and Backend simultaneously (Optional but recommended extra).
- `cd frontend && npm run dev`: Start Next.js development server.
- `cd frontend && npm run test`: Run frontend unit tests.
- `cd backend && uv sync`: Install backend dependencies and set up the virtual environment.
- `cd backend && uv run uvicorn main:app --reload`: Start FastAPI backend.
- `cd backend && uv run pytest`: Run backend unit tests.
- `cd backend && uv run python seed.py`: Initialize the SQLite database with 10 pre-registered tickets.

## Architecture

- `/` (Root): Monorepo configuration and shared setups (e.g., `docker-compose.yml`).
- `/frontend/app`: Next.js App Router containing `/tickets` and `/dashboard` interfaces.
- `/frontend/__tests__`: Frontend unit tests for components and utilities.
- `/backend`: Python FastAPI application housing the core API and LLM logic.
- `/backend/tests`: Backend unit tests for API endpoints and AI services.
- `/backend/database`: SQLite `.db` file managed via a named Docker volume.
- `/backend/services/ai`: Integration layer with the LLM (Gemini).

## Database Logic

The backend automatically manages its persistence layer:
- **Automatic Initialization:** On startup, the system checks for an existing tickets database.
- **Seeding:** If no database is found, it automatically creates one and populates it with 10 dummy records, each classified and prioritized by the AI service.
- **Configurability:** Database location is controlled via the `DATABASE_PATH` environment variable, ensuring seamless integration with Docker volumes.

## API Documentation

The backend API is served by default at `http://localhost:8000`.

### 1. List All Tickets
*   **Endpoint:** `GET http://localhost:8000/tickets`
*   **Description:** Retrieves a list of all support tickets stored in the database.
*   **Output (JSON):** A list of objects containing `id`, `customer_name`, `message`, `status`, `priority`, and `category`.

### 2. Create Support Ticket
*   **Endpoint:** `POST http://localhost:8000/tickets`
*   **Description:** Creates a new ticket. The backend automatically classifies the `category` and `priority` using the Gemini AI service.
*   **Input (JSON):**
    ```json
    {
      "customer_name": "string",
      "message": "string"
    }
    ```
*   **Output (JSON):** The created ticket object including AI-generated fields.

### 3. Update Support Ticket
*   **Endpoint:** `PATCH http://localhost:8000/tickets/{ticket_id}`
*   **Description:** Updates the `status` or `priority` of an existing ticket.
*   **Input (JSON):**
    ```json
    {
      "status": "string (optional: 'pending' or 'resolved')",
      "priority": "string (optional: 'low' or 'high')"
    }
    ```
*   **Output (JSON):** The updated ticket object.

### 4. Draft AI Answer
*   **Endpoint:** `POST http://localhost:8000/tickets/{ticket_id}/draft`
*   **Description:** Generates a drafted response for the specified ticket using AI. Only available for tickets with 'pending' status.
*   **Output (JSON):**
    ```json
    {
      "draft": "string"
    }
    ```

## Important Notes

- **Monorepo Structure:** Both the frontend and backend reside in this single repository. Keep dependency management cleanly separated between the two environments.
- **Environment Variables & Security:** All sensitive information MUST be stored in environment variables. NEVER commit `.env` files to version control.
- **LLM Integration:** The API key for Gemini is located in the `.env` file. The backend must intercept the `POST /tickets` message and send it to the Gemini API (model `gemini-3.1-flash-lite-preview`) before saving to the database.
- **Gemini Model:** The project specifically utilizes the `gemini-3.1-flash-lite-preview` version for both ticket classification and response drafting.
- LLM Output: The AI must return a structured JSON containing a `category` and a suggested `priority` ("low" or "high") based on the message tone.
- API Endpoints: The backend must expose `GET /tickets`, `POST /tickets` (receiving only `customer_name` and `message`), and `PATCH /tickets/{id}` (to update status or priority).
- Documentation is Critical: The `README.md` must contain extremely clear instructions on how to run the project locally, how to execute the test suites, and how to configure the `.env` file (e.g., providing a `.env.example`).
