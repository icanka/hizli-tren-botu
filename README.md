# YHSTBOT - Yüksek Hızlı Tren Telegram Botu - TCDD HIZLI TREN BOT - YHT Bot

[![GitHub stars](https://img.shields.io/github/stars/icanka/hizli-tren-botu?style=social)](https://github.com/icanka/hizli-tren-botu/stargazers)
[![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

Find and book **TCDD YHT (Yüksek Hızlı Tren)** high-speed train tickets from Telegram.

## Quick start

Export `BOT_TOKEN` and `AUTH_USER_IDS` before starting Docker Compose:

```bash
export BOT_TOKEN=<telegram_bot_token>
export AUTH_USER_IDS=1234567,1234567,123467  # comma delimited allowed user ids
```

```bash
docker compose up -d
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for local development and production setup.

## Usage

Message [@YHSTBOT](https://t.me/YHSTBOT) on Telegram and send `/start` to begin a conversation with the bot.

### Inline functions

- `@YHSTBOT query pendik ankara 17ekim15:30` — set the trip to search for
- `@YHSTBOT stations` — list available YHT stations

## License

GPL-3.0. See [LICENSE](LICENSE).

---

If this project is useful to you, a ⭐ helps others find it.
