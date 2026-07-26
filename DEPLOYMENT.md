# YHSTBOT - Deployment & Operational Guide

This document provides a comprehensive guide to setting up, running, and deploying **YHSTBOT** (Yüksek Hızlı Tren Telegram Botu) for TCDD High-Speed Train ticket monitoring and reservations.

---

## 🏗️ Architecture Overview

The system consists of three main components managed via Docker Compose:

```
                  +-----------------------+
                  |     Telegram User     |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  |   bot (Telegram App)  |
                  |  (src/__main__.py)    |
                  +-----------+-----------+
                              |
                              | Queues Tasks
                              v
                      +---------------+
                      | Redis Broker  |
                      | (redis:6379)  |
                      +-------+-------+
                              |
                              | Consumes Tasks
                              v
                  +-----------------------+
                  |     celery worker     |
                  | (tasks/celery_tasks)  |
                  +-----------------------+
```

1. **`bot` (Telegram Bot Service)**:
   - Runs `src/__main__.py` with `python-telegram-bot` and `APScheduler`.
   - Manages user sessions, inline queries, interactive menus, and persistence (`/bot_data/my_persistence`).
   - Access is restricted to user IDs defined in `AUTH_USER_IDS`.

2. **`celery` (Background Worker Service)**:
   - Runs `celery -A tasks.celery_tasks worker` to execute periodic or long-running TCDD train search tasks asynchronously.

3. **`redis` (Broker & State Storage)**:
   - Redis 7 (Alpine) container used as the message broker and result store for Celery tasks.

---

## 📋 Prerequisites

- **Docker & Docker Compose** (v2.20+)
- **Telegram Bot Token**: Created via [@BotFather](https://t.me/BotFather) on Telegram.
- **Authorized Telegram User IDs**: Your numeric Telegram ID (get it from [@userinfobot](https://t.me/userinfobot)).

---

## 🚀 Quick Start (Docker Compose Deployment)

### 1. Clone & Navigate to Repository
```bash
git clone https://github.com/icanka/hizli-tren-botu.git
cd hizli-tren-botu
```

### 2. Set Environment Variables
Export your Telegram Bot Token and authorized user ID(s):

```bash
export BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyZ"
export AUTH_USER_IDS="123456789,987654321"  # Comma-separated for multiple users
```

*(Optional: Create a `.env` file in the project root)*:
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyZ
AUTH_USER_IDS=123456789,987654321
```

### 3. Build & Start Services
```bash
docker compose up -d --build
```

### 4. Verify Service Health
Check running containers and logs:
```bash
docker compose ps
docker compose logs -f bot
```

---

## 💻 Local Development Setup (Without Docker)

If you wish to run and debug the bot locally:

### 1. Create & Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Start Local Redis Server
Ensure Redis is installed and running on port `6379`:
```bash
redis-server
```

### 3. Start Celery Worker
In a new terminal window (with `.venv` activated and `PYTHONPATH=src`):
```bash
export PYTHONPATH=src
celery -A tasks.celery_tasks worker -c 1 --loglevel=INFO
```

### 4. Start Telegram Bot
In another terminal window:
```bash
export BOT_TOKEN="your_bot_token"
export AUTH_USER_IDS="your_telegram_id"
export PERSISTENCE_FILE_PATH="bot_data/my_persistence"
export PYTHONPATH=src

python3 src/__main__.py
```

---

## 🔒 Production Best Practices

### 1. Systemd Service (Automatic Startup on Boot)
To ensure the bot automatically starts when your Linux server boots up, create a systemd service file:

`/etc/systemd/system/yhstbot.service`:
```ini
[Unit]
Description=YHSTBOT Telegram Bot & Celery Worker
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/hizli-tren-botu
Environment="BOT_TOKEN=your_telegram_bot_token"
Environment="AUTH_USER_IDS=your_telegram_id"
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now yhstbot
```

### 2. Data Persistence & Backups
All persistent state and logs are stored in the `./bot_data/` directory:
- `/bot_data/my_persistence`: Telegram bot conversation states & user settings.
- `/bot_data/logs/`: Application logs for bot and Celery.

**Backup recommendation**: Periodically back up `./bot_data/my_persistence`.

### 3. Security Considerations
- **Restrict Access**: Only list trusted Telegram user IDs in `AUTH_USER_IDS`. Unlisted users will be denied access to the bot.
- **Environment Secrets**: Never commit `.env` or plain-text tokens to Git repositories.

---

## 🛠️ Maintenance & Useful Commands

| Task | Command |
|---|---|
| View Bot Logs | `docker compose logs -f bot` |
| View Celery Logs | `docker compose logs -f celery` |
| View Redis Logs | `docker compose logs -f redis` |
| Restart All Services | `docker compose restart` |
| Rebuild Containers | `docker compose up -d --build` |
| Check Pylint Code Quality | `.venv/bin/pylint $(git ls-files '*.py')` |
