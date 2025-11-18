# Package Tracker Frontend

A React-based frontend application for tracking shipping packages. Built with Vite and styled with Tailwind CSS.

## Features

- **Authentication System**
  - User registration
  - Login/Logout
  - Forgot password
  - Reset password
  
- **Package Management**
  - View all tracked packages
  - Add new packages with tracking numbers
  - Select carrier from dropdown
  - Delete packages
  - Display latest status and updates

- **Responsive Design**
  - Mobile-friendly interface
  - Grid layout for package cards
  - Modal dialogs for forms

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS v3** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

## Prerequisites

- Node.js 18+ 
- npm or yarn
- FastAPI backend running on `http://localhost:8000`

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173/`

## Build for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   └── AddPackageModal.jsx
│   ├── pages/              # Page components
│   │   ├── AuthView.jsx    # Authentication page
│   │   └── Dashboard.jsx   # Main dashboard
│   ├── services/           # API service layer
│   │   └── api.js          # Axios configuration and API calls
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # Application entry point
│   └── index.css           # Global styles and Tailwind imports
├── public/                 # Static assets
├── index.html             # HTML template
├── tailwind.config.js     # Tailwind configuration
├── postcss.config.js      # PostCSS configuration
└── vite.config.js         # Vite configuration
```

## API Integration

The frontend communicates with a FastAPI backend on `http://localhost:8000`. JWT tokens are automatically included in requests via Axios interceptors.

### Required Backend Endpoints

**Authentication:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token

**Packages:**
- `GET /packages` - Get all packages (requires auth)
- `POST /packages` - Add new package (requires auth)
- `DELETE /packages/{id}` - Delete package (requires auth)
- `PUT /packages/{id}` - Update package (requires auth)

**Carriers:**
- `GET /carriers` - Get list of supported carriers

## Environment Configuration

To change the API base URL, edit `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Authentication

The app uses JWT token-based authentication. Tokens are stored in `localStorage` and automatically included in API requests via Axios interceptors.

## License

MIT
