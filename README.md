# Quran Hub — Islamic Learning Platform

A modern, full-stack Islamic learning platform with Admin CMS & AI Tutor capabilities.

## Project Overview

**Quran Hub** is a comprehensive Islamic education platform featuring:
- 📖 **Quran** — Complete Quran with Surah and Ayah details
- 🕌 **Hadith** — Collections (Bukhari, Muslim, etc.)
- 🔍 **Tafsir** — Scholarly interpretations
- 📜 **Sirah** — Islamic history and biography
- 🤖 **AI Tutor** — Intelligent Q&A about Islamic content

## Tech Stack

### Frontend
- **React 18** + TypeScript
- **TailwindCSS** for styling
- **React Router v6** for navigation
- **TipTap** WYSIWYG editor
- **Lucide React** for icons
- **DOMPurify** for HTML sanitization

### Backend
- **FastAPI** (Python 3.11+)
- **Motor** async MongoDB driver
- **Pydantic** for data validation
- **PyJWT** for authentication
- **bcrypt** for password hashing
- **bleach** for HTML sanitization

### Database
- **MongoDB** with Docker

### AI Integration
- Support for OpenAI GPT, Google Gemini, Anthropic Claude
- Abstraction layer for provider switching via environment variables

## Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker & Docker Compose

### Setup

```bash
# Clone and navigate
git clone https://github.com/aqsastudycommunity24/Tes.git
cd Tes

# Start all services
docker-compose up -d

# Initialize database
cd backend
python seed.py

# Access
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# MongoDB: localhost:27017
```

### Default Credentials
- **Email**: admin@qurahub.test
- **Password**: AdminPassword123!

## Project Structure

```
quran-hub/
├── frontend/              # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utility functions
│   │   └── App.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile.dev
│   └── .env.example
├── backend/               # FastAPI + Python
│   ├── app/
│   │   ├── api/           # API routes
│   │   │   ├── auth.py
│   │   │   ├── contents.py
│   │   │   ├── admin.py
│   │   │   └── ai.py
│   │   ├── models/        # Pydantic models
│   │   ├── db/            # Database layer
│   │   ├── middleware/    # Middleware
│   │   ├── utils/         # Utility functions
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── seed.py
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://mongodb:27017/quran-hub
JWT_SECRET=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
JWT_REFRESH_EXPIRATION_DAYS=7

LLM_PROVIDER=openai  # or gemini, claude
LLM_API_KEY=your-api-key

CORS_ORIGINS=http://localhost:5173,http://localhost:3000

RATE_LIMIT_LOGIN=5/minute
RATE_LIMIT_AI=10/minute
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Quran Hub
```

## Design System

### Colors
- **Primary**: Deep Green `#0F3830`
- **Accent**: Soft Gold `#D4AF37`
- **Background**: Light Gray `#F8F8F8`
- **Text**: Dark Gray `#1F2937`

### Typography
- **UI Font**: Comic Neue
- **Arabic Text**: Amiri or Scheherazade

### Features
- 🌙 Dark Mode with localStorage persistence
- 📱 Mobile-first responsive design
- ♿ Accessibility-first
- 🎨 Smooth transitions

## Development

### Backend Dev Mode
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Dev Mode
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/login` — Admin login
- `POST /api/auth/refresh` — Refresh token
- `POST /api/auth/logout` — Logout

### Content (Public)
- `GET /api/contents` — List contents
- `GET /api/contents/{slug}` — Get single content

### Admin
- `POST /api/admin/contents` — Create content
- `PUT /api/admin/contents/{id}` — Update content
- `DELETE /api/admin/contents/{id}` — Delete content
- `POST /api/admin/upload-html` — Upload HTML file
- `GET/POST/PUT/DELETE /api/admin/users` — User management

### AI Tutor
- `POST /api/ai/chat` — Send message with streaming

## Database Schema

### users
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password_hash: String,
  name: String,
  role: String (superadmin|editor|contributor),
  created_at: DateTime,
  updated_at: DateTime
}
```

### contents
```javascript
{
  _id: ObjectId,
  pillar: String (quran|hadith|tafsir|sirah),
  category: String,
  title: String,
  slug: String (unique),
  html_body: String,
  tags: [String],
  cover_image: String,
  status: String (draft|published),
  author_id: ObjectId,
  created_at: DateTime,
  updated_at: DateTime,
  deleted_at: DateTime
}
```

### ai_conversations
```javascript
{
  _id: ObjectId,
  user_session: String,
  messages: [
    {
      role: String (user|assistant),
      content: String,
      timestamp: DateTime
    }
  ],
  context_content_id: ObjectId,
  created_at: DateTime
}
```

### audit_logs
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  action: String (create|update|delete),
  resource_type: String,
  resource_id: ObjectId,
  changes: Object,
  timestamp: DateTime
}
```

## Security

✅ JWT authentication with access & refresh tokens
✅ Password hashing with bcrypt
✅ HTML sanitization (DOMPurify + bleach)
✅ CORS whitelist protection
✅ Rate limiting on sensitive endpoints
✅ Role-Based Access Control (RBAC)

## Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Superadmin** | Full access + user management |
| **Editor** | CRUD all content |
| **Contributor** | Create drafts only |

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit: `git commit -am 'Add feature'`
3. Push: `git push origin feature/your-feature`
4. Submit PR

## License

MIT License

## Support

Open an issue on GitHub for questions and bugs.

---

**Made with ❤️ for Islamic Education**