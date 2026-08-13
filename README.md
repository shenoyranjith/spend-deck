# SpendDeck

SpendDeck is a self-hosted credit-card spending dashboard for category analysis,
milestone estimation, and reward tracking.

This repository currently contains the project foundation:

- Django and Django REST Framework API
- SQLite runtime storage
- Versioned YAML card catalogue with strict validation
- React, TypeScript, Vite, and Tailwind CSS frontend
- Single-container production build

## Requirements

- Python 3.12+
- Node.js 22.12+
- npm 10+
- Docker and Docker Compose (optional)

## Local setup

```bash
make setup
make migrate
```

Run the backend and frontend in separate terminals:

```bash
make dev-backend
make dev-frontend
```

Open `http://localhost:5173`. Vite proxies `/api` requests to Django on port
`8000`.

If you use nvm, run `nvm use` from the repository root before `make setup`.

## Checks

```bash
make check
```

## Docker

```bash
docker compose up --build
```

Open `http://localhost:8000`. Runtime data is stored in the named
`spenddeck-data` volume.

## Catalogue layout

Shipped card knowledge lives in Git, separate from private user data:

```text
catalog/cards/<issuer>/<card>/card.yaml
catalog/cards/<issuer>/<card>/rules/<effective-date>.yaml
```

`catalog/examples/demo_card` documents the current schema but is not loaded as
a supported card. Validate catalogue changes with:

```bash
make catalogue-check
```
