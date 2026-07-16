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

### Environment variables

```bash
cp .env.example .env
```

Edit `.env` as needed. Settings read `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` from there.

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deploy to PythonAnywhere (mkmsater)

Account: [pythonanywhere.com](https://www.pythonanywhere.com)  
Live URL: `https://mkmsaterg.pythonanywhere.com`

### 1. Clone and install (Bash console)

```bash
cd ~
git clone https://github.com/MKmasterg/coffee-market-place.git
cd coffee-market-place
mkvirtualenv --python=/usr/bin/python3.10 coffee-env
pip install -r requirements.txt
```

### 2. Create `.env` on the server

```bash
cd ~/coffee-market-place
nano .env
```

```bash
export SECRET_KEY=your-generated-secret-key
export DEBUG=False
export ALLOWED_HOSTS=mkmsater.pythonanywhere.com
```

Load `.env` in Bash consoles (run once):

```bash
echo 'set -a; source ~/coffee-market-place/.env; set +a' >> ~/.virtualenvs/coffee-env/bin/postactivate
```

### 3. Database and static files

```bash
workon coffee-env
cd ~/coffee-market-place
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 4. Web app (Web tab)

| Setting | Value |
|---------|--------|
| Config | Manual, Python 3.10 |
| Virtualenv | `coffee-env` |
| Source / working dir | `/home/mkmsaterg/coffee-market-place` |
| Static URL | `/static/` |
| Static directory | `/home/mkmsaterg/coffee-market-place/staticfiles` |

Paste WSGI from `deploy/pythonanywhere_wsgi.py`, then **Reload**.


**Manual deploy:** Actions tab → Deploy to PythonAnywhere → Run workflow.

Workflow file: `.github/workflows/deploy.yml` — runs `git pull`, `pip install`, `migrate`, `collectstatic`, reload.

### 5. Manual updates (without CI)

```bash
workon coffee-env
cd ~/coffee-market-place
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Reload the web app on the Web tab.

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
