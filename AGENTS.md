# AGENTS.md

Guidance for AI coding agents working on this repository.

## Project

YHSTBOT (Yüksek Hızlı Tren Telegram Botu) — a Telegram bot that searches for
TCDD high-speed train (YHT) tickets. Users interact through commands and inline
queries; long-running searches run asynchronously.

Stack: Python 3.13, `python-telegram-bot`, APScheduler, Celery + Redis, Docker Compose.

## Layout

- `src/` — bot source code
  - `src/__main__.py` — bot entry point
  - `src/tasks/` — Celery tasks (async TCDD searches)
  - `src/telegram_bot.py`, `src/update_processor.py` — bot wiring and handlers
- `docker-compose.yaml` — `bot`, `celery`, and `redis` services
- `DEPLOYMENT.md` — full local-dev and production deployment guide
- `README.md` — quick start

## Running

Docker (recommended):

```bash
export BOT_TOKEN=<telegram_bot_token>
export AUTH_USER_IDS=<comma,separated,telegram_ids>
mkdir -p bot_data/logs
docker compose up -d --build
```

Local development and troubleshooting are documented in `DEPLOYMENT.md`.

## Checks

- Lint: `pylint $(git ls-files '*.py')` (same command as the Pylint workflow)
- There is no automated test suite; verify changes by running the bot locally.

## Conventions

- Keep changes focused and follow the existing structure in `src/`.
- Never commit tokens, `.env` files, or other secrets.
- Pylint configuration lives in `.pylintrc`.

## Attribution

This repository participates in the AI Attribution Protocol. See
[`ATTRIBUTION.md`](ATTRIBUTION.md) for reciprocity guidelines.
