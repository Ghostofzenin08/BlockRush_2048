# 🚀 BlockRush 2048

<div align="center">

![BlockRush Logo](goz_logo_light.png)

### *Cyberpunk-Themed Competitive 2048 with Dynamic Grids, Progression Tiers, and Real-Time Cloud Sync*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon_DB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://neon.tech)
[![Firebase](https://img.shields.io/badge/Firebase-Auth-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Render](https://img.shields.io/badge/Render-Live_Production-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://blockrush-2048.onrender.com)
[![itch.io](https://img.shields.io/badge/itch.io-Playable_Release-FA5C5C?style=for-the-badge&logo=itch.io&logoColor=white)](https://zeninxparth.itch.io/blockrush-2048)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

### 🎮 **[Play Live on Render](https://blockrush-2048.onrender.com/)** &nbsp; | &nbsp; 🕹️ **[Play on itch.io](https://zeninxparth.itch.io/blockrush-2048)** &nbsp; | &nbsp; 💻 **[Download Windows .exe](https://zeninxparth.itch.io/blockrush-2048)**

</div>

---

## 📖 Overview

**BlockRush 2048** reimagines the classic mathematical sliding tile puzzle into an exhilarating, competitive cyber-arcade experience. Featuring dark glassmorphism aesthetics, dynamic board scaling from 2x2 up to 12x12, real-time Firebase Authentication, cross-platform cloud score persistence via Neon PostgreSQL, and competitive tier rankings.

Whether you prefer playing directly in the browser via WebGL/HTML5 or through the standalone high-performance Windows desktop client (Pygame engine), BlockRush delivers fluid 60fps animations, reactive SFX, and global leaderboards.

---

## ✨ Key Features

- 📐 **Dynamic Grid Sizes (2x2 to 12x12)**: Play on the classic 4x4, quick reflex 3x3, or intense mega-boards up to 12x12 with adaptive tile fonts and responsive spacing.
- 🎨 **Sleek Cyberpunk UI / Glassmorphism**: Designed with dark frosted glass (`backdrop-filter: blur(24px)`), neon accents (`#6366F1`, `#EC4899`, `#10B981`), glowing tier badges, and clean `Instrument Sans` typography.
- 🏆 **Competitive Progression & Rank Tiers**: Real-time rank progression that evaluates your performance:
  - 🥉 **Bronze** (0 - 999 pts)
  - 🥈 **Silver** (1,000 - 2,499 pts)
  - 🥇 **Gold** (2,500 - 4,999 pts)
  - 💠 **Platinum** (5,000 - 9,999 pts)
  - 💎 **Diamond** (10,000 - 24,999 pts)
  - 👑 **Master** (25,000 - 49,999 pts)
  - ⚡ **Immortal** (50,000+ pts)
- 🔐 **Dual Auth (Google & Email/Password)**: Secure Firebase Auth integrated seamlessly into a custom neon glass popup with profile management, guest play, and session persistence.
- 🌐 **Robust Cloud Sync + Offline Fallback**: High-availability persistence powered by **Neon PostgreSQL** with automated connection pooling and fallback to localized JSON storage whenever offline.
- 🔊 **Synthesized SFX Engine**: Dynamic sound effects for sliding, combining tiles, milestones, and game over states.
- 📱 **Fully Responsive & Cross-Platform**:
  - Touch-swipe support for mobile & tablet.
  - Arrow keys & WASD controls for desktop.
  - Native Windows `.exe` desktop application with custom multi-resolution icon.

---

## 🏗️ Architecture & Technology Stack

```
                                 ┌───────────────────────────────┐
                                 │       BlockRush Clients       │
                                 └───────────────┬───────────────┘
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     ▼                                                       ▼
        ┌─────────────────────────┐                             ┌─────────────────────────┐
        │     HTML5 / JS Client   │                             │  Desktop Python/Pygame  │
        │   (Web & itch.io Web)   │                             │   (Windows Standalone)  │
        └────────────┬────────────┘                             └────────────┬────────────┘
                     │                                                       │
                     │ (Firebase Auth / REST API)                            │ (Local / API Sync)
                     ▼                                                       ▼
        ┌─────────────────────────────────────────────────────────────────────────────────┐
        │                     Flask 3.0+ WSGI Backend Service                             │
        │               (Render Cloud / Gunicorn / Python 3.11.9)                         │
        └────────────────────────────────────────┬────────────────────────────────────────┘
                                                 │
                     ┌───────────────────────────┴───────────────────────────┐
                     ▼                                                       ▼
        ┌─────────────────────────┐                             ┌─────────────────────────┐
        │    Neon PostgreSQL      │                             │   Local JSON Storage    │
        │   (Serverless Cloud)    │                             │   (Graceful Fallback)   │
        └─────────────────────────┘                             └─────────────────────────┘
```

### Stack Details
| Layer | Technologies |
| :--- | :--- |
| **Frontend Web** | Vanilla ES6+ JavaScript, CSS3 Variables, Glassmorphism, SVG Icons |
| **Desktop Client** | Python 3.11, Pygame Engine, Pillow, PyInstaller |
| **Backend API** | Flask 3.0, Gunicorn, Flask-CORS, Flask-SQLAlchemy 3.x |
| **Authentication** | Firebase Authentication v10 (Google OAuth + Email/Password) |
| **Database** | Neon Serverless PostgreSQL (Cloud) / Local JSON fallback |
| **Cloud Hosting** | Render (Web Service), itch.io (HTML5 & Windows Bundle) |

---

## 📁 Repository Structure

```
BlockRush_2048/
├── assets/                  # UI icons, SVG assets, and sound effects
├── backend/                 # Flask backend service
│   ├── app/
│   │   ├── models/          # Database models (User, Score, Leaderboard)
│   │   ├── routes/          # API route controllers (auth, game, health)
│   │   ├── services/        # DB sync & JSON fallback services
│   │   └── __init__.py      # Flask application factory
│   └── requirements.txt     # Python backend dependencies
├── dist/                    # Compiled Windows desktop releases
├── docs/                    # Architecture, PRD, and design system specs
├── src/                     # Pygame native desktop engine
│   ├── constants.py         # Grid colors, tile values, dimensions
│   ├── game_logic.py        # Core sliding tile matrix algorithm
│   ├── main.py              # Pygame application entrypoint
│   └── ui.py                # Desktop GUI renderer & HUD
├── .env.example             # Environment variable template
├── .gitignore               # Ignored build artifacts, venv, and secrets
├── .python-version          # Python 3.11.9 pin for Render build environment
├── BlockRush2048_Single.spec# PyInstaller single-file build specification
├── firebase-config.js       # Firebase SDK initialization & API origin resolution
├── index.html               # Main HTML5 game client & auth modal
├── requirements.txt         # Root dependency list for Render / WSGI
├── script.js                # Core web game engine, keyboard/touch input, API calls
├── styles.css               # Dark theme, glassmorphism, responsive grid layout
└── wsgi.py                  # Production WSGI entrypoint with sys.path configuration
```

---

## 🕹️ Controls & How to Play

### Objective
Slide numbered tiles across the board. When two tiles with the same number collide during a move, they **merge into one** with the sum of their values (2 + 2 = 4, 4 + 4 = 8, ..., 1024 + 1024 = 2048!).

### Controls
| Platform | Input / Action |
| :--- | :--- |
| **Desktop / Web** | <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> or <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd> |
| **Mobile / Touch** | Swipe in the desired slide direction |
| **New Game** | Click **New Game** button or press <kbd>R</kbd> |
| **Change Grid Size** | Select dimension (2x2 to 12x12) from dropdown |
| **Sign In / Out** | Click the profile icon in the top header |

---

## 🔌 API Endpoints

The Flask backend provides RESTful endpoints used by both the Web and Desktop clients:

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/health` | Cloud health check & database connection probe | No |
| `GET` | `/api/leaderboard` | Retrieve top scores filtered by grid size | No |
| `POST` | `/api/save-score` | Submit game score, max tile, and moves | Optional |
| `GET` | `/api/user-stats` | Fetch user career stats and rank tier | Optional |

---

## 🚀 Local Development Setup

### 1. Prerequisites
- **Python 3.11+** installed
- **Git** installed

### 2. Clone the Repository
```bash
git clone https://github.com/Ghostofzenin08/BlockRush_2048.git
cd BlockRush_2048
```

### 3. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy .env.example .env

# Run local development server
python wsgi.py
```
The backend will run at `http://127.0.0.1:5000/`. You can verify by opening `http://127.0.0.1:5000/health`.

### 4. Running the Web Game Locally
Serve the root directory using any local web server:
```bash
# Using Python built-in HTTP server:
python -m http.server 8080
```
Open `http://localhost:8080` in your web browser.

### 5. Running the Pygame Desktop Client
```bash
python src/main.py
```

---

## 📦 Building Standalone Windows Executable

To compile a standalone portable `.exe` with embedded icon and assets:

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the spec file
pyinstaller BlockRush2048_Single.spec
```
The compiled single-file executable will be output to:
`dist/BlockRush.exe`

---

## 🌐 Cloud Deployment & Publishing

### Render (Live Backend Service)
- **Runtime**: Python 3 (pinned via `.python-version` to `3.11.9`)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app`
- **Environment Variables**:
  - `DATABASE_URL`: Neon PostgreSQL connection string (`postgresql://...`)
  - `FLASK_ENV`: `production`

### itch.io (HTML5 Web Bundle)
When packaging for itch.io web uploads:
- Ensure all relative asset links in the zip archive use forward slashes (`assets/play.svg`), avoiding Windows-style backslashes (`\`).
- Authorized domains in Firebase Authentication must include:
  - `onrender.com`
  - `itch.io`
  - `itch.zone`

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.

---

<div align="center">
  <sub>Crafted with passion for puzzle games & competitive arcade experiences.</sub>
</div>
