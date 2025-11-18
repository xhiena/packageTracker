# Package Tracker

A simple shipping package tracker with a React frontend and FastAPI backend.

## Project Structure

```
packageTracker/
├── frontend/          # React application (Vite + Tailwind CSS)
└── README.md         # This file
```

## Frontend

The frontend is a React-based web application built with:
- React 18
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (API client)

### Quick Start

```bash
cd frontend
npm install
npm run dev
```

See [frontend/README.md](frontend/README.md) for detailed documentation.

## Features

- **User Authentication**: Register, login, forgot/reset password
- **Package Tracking**: Add packages with tracking numbers and carriers
- **Dashboard**: View all tracked packages with latest status
- **Responsive Design**: Works on desktop and mobile devices

## Development Setup

1. Start the FastAPI backend on port 8000 (if available)
2. Start the React frontend:
   ```bash
   cd frontend
   npm run dev
   ```
3. Open http://localhost:5173 in your browser

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Axios
- **Backend**: FastAPI (port 8000)
- **Authentication**: JWT tokens

## License

MIT
