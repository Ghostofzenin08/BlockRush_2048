# AI System Memory & State Management (Memory.md)

## 1. Overview & Context Preservation
This document defines the system memory, decision log, and session context rules for AI coding assistants working on the Flask & BlockRush codebase.

---

## 2. Active Session Context & State

| Parameter | Current State | Notes |
| :--- | :--- | :--- |
| **Project Name** | BlockRush | Interactive 2048 Puzzle Game & Web Portal |
| **Backend Stack** | Python 3.11+ / Flask 3.0+ / Flask-SQLAlchemy | Flask Application Factory pattern |
| **Database** | PostgreSQL on Neon DB | Serverless, SSL mode `require`, pooled connection |
| **Frontend Stack** | HTML5, Tailwind CSS, JavaScript | Single Page Application router (`index.html`) |
| **Figma Node** | `594-2` | Primary design specification |
| **Primary Fonts** | `Instrument Sans`, `Inria Sans` | Applied globally |

---

## 3. Key Decision Log
- **2026-09-09**: Initialized full 13-document Prompt Engineering specification suite based on `parthongit89/Project-Strategies-Prompt-engineering-` repository.
- **2026-09-09**: Enforced `Flask-JWT-Extended` for authentication and `Flask-Talisman` for security headers.
- **2026-09-09**: Verified Figma node `594-2` visual layout compliance across Main Menu, Game Viewport, Weekly Challenge, Playground Math Level, and BlockDocs Support pages.
