# Coffee Market Place

A Django marketplace where sellers/supervisors manage markets and stock, and customers browse and place orders.

## Roles

- **Seller / Supervisor** — manage stock, orders, and market settings
- **Customer** — browse markets and place orders
- **No role** — new users are prompted to pick a role after signup

New markets need admin approval (`is_verified`) before they appear to users.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Project layout

```
coffee-market-place/
├── manage.py
├── CoffeeMarketPlace/   # project settings & URLs
├── users/               # auth, roles, customers, sellers
├── markets/             # market pages, stock, orders
└── templates/           # shared templates
```

## Notes

- Dev DB is SQLite (`db.sqlite3`) — gitignored; run `migrate` after clone
- Still in development; contributions welcome
