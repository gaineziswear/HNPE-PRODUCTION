# HNPE Production — Ultra-Advanced Trading Signal Platform (Full scaffold)

This archive contains a complete scaffold of the HNPE trading-signal platform:
- FastAPI backend
- Next.js frontend (skeleton)
- Telegram bot
- Docker compose + Dockerfiles
- Database schema & migrations
- CI workflows
- Scripts and docs

Quickstart (dev)
1. Copy `.env.example` to `.env` and fill secrets.
2. Build & run: `docker compose up --build`
3. Backend API: http://localhost:8000/docs
4. Frontend: http://localhost:3000
5. Telegram bot: configure `TELEGRAM_BOT_TOKEN`

See `docs/SETUP.md` for more details.
