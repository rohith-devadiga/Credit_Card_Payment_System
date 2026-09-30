# Credit Card Payment System (Backend)

A backend payment simulation system exposing REST APIs.

**Stack:** Django REST Framework (auth, cards, transactions, admin) · FastAPI (payment processing) · MySQL

## Architecture

```
API client (Postman / curl / any frontend)
   |
   |--> Django API (:8000)   -- auth, cards, transaction history, admin panel
   |--> FastAPI (:8001)      -- payment processing only
                 |
              MySQL (:3306)  -- shared database, schema owned by Django migrations
```

Both services share one MySQL database. Django owns the schema (via migrations); FastAPI reads/writes to the `cards_card` and `transactions_transaction` tables through SQLAlchemy models mapped to those same table names. Both services validate the same JWT (same `SECRET_KEY` + `HS256`), so a token issued by Django's `/api/auth/login/` also authenticates FastAPI's `/api/payments/`.

## Setup (Docker — recommended)

```bash
cp backend_django/.env.example backend_django/.env

docker-compose up --build
```

- Django API: http://localhost:8000/api
- FastAPI docs (Swagger): http://localhost:8001/docs
- Create an admin user: `docker-compose exec django python manage.py createsuperuser`

## Setup (manual / local dev)

**Django**
```bash
cd backend_django
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit MYSQL_HOST=localhost if running MySQL locally
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

**FastAPI**
```bash
cd backend_fastapi
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export MYSQL_HOST=localhost DJANGO_SECRET_KEY=<same value as backend_django/.env>
uvicorn main:app --reload --port 8001
```

## Running Tests

```bash
# Django (auth, cards, transactions, admin panel)
cd backend_django && python manage.py test

# FastAPI (payment simulation logic)
cd backend_fastapi && pytest
```

## API Documentation

- **FastAPI:** Swagger UI auto-generated at `/docs`, ReDoc at `/redoc`.
- **Django:** endpoints are listed below; a Postman collection (`postman_collection.json`) covering every endpoint is included at the repo root — import it into Postman and set the `access_token` collection variable after logging in.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | none | Create a user |
| POST | `/api/auth/login/` | none | Get access + refresh JWT |
| POST | `/api/auth/logout/` | user | Blacklist refresh token |
| GET | `/api/auth/me/` | user | Current user (protected route) |
| GET/POST | `/api/cards/` | user | List / add cards |
| DELETE | `/api/cards/<id>/` | user | Delete a card |
| POST | `/api/payments/` (FastAPI, :8001) | user | Make a payment |
| GET | `/api/transactions/` | user | History, filterable by `status`, `date_from`, `date_to`, `min_amount`, `max_amount` |
| GET | `/api/transactions/export/` | admin | CSV export |
| GET | `/api/admin-panel/users/` | admin | Manage users |
| GET | `/api/admin-panel/cards/` | admin | View all cards |
| GET | `/api/admin-panel/transactions/` | admin | View all transactions |
| GET | `/api/admin-panel/summary/` | admin | Daily payment summary |

## Database Schema

**users** *(Django's built-in `auth_user`)* — id, username, email, password (hashed), is_staff, date_joined

**cards_card**
| column | type | notes |
|---|---|---|
| id | PK | |
| user_id | FK -> auth_user | |
| card_holder_name | varchar | |
| brand | varchar | VISA / MASTERCARD / AMEX / OTHER |
| last4 | varchar(4) | |
| masked_number | varchar | e.g. `**** **** **** 1234` |
| expiry_month / expiry_year | int | |
| created_at | datetime | |

*Full card numbers and CVVs are never received into a stored field or written to disk — only `last4` and a masked display string persist.*

**transactions_transaction**
| column | type | notes |
|---|---|---|
| id | PK | |
| reference_id | UUID | unique |
| user_id | FK -> auth_user | |
| card_id | FK -> cards_card | nullable |
| amount | decimal(12,2) | |
| currency | varchar(3) | |
| status | varchar | PENDING / SUCCESS / FAILED |
| failure_reason | varchar | |
| created_at / updated_at | datetime | |

**Admin Logs**: covered by Django's built-in `django_admin_log` table, populated automatically for any action taken through `/admin/`.

## Security Notes (Module 8)

- No CVV is ever accepted or stored by any endpoint.
- Passwords are hashed with Django's PBKDF2 hasher (`set_password`) — never stored in plaintext.
- Auth uses JWT (`djangorestframework-simplejwt`) with access/refresh tokens and blacklist-on-logout.
- All input is validated through DRF/Pydantic serializers before touching the database.
- SQL injection protection: Django ORM and SQLAlchemy's parameterized queries are used exclusively — no raw string-interpolated SQL anywhere in the codebase.

## Admin Credentials (for submission)

After running `createsuperuser`, note the chosen username here for the reviewer, e.g.:
```
username: admin
password: Rdevadiga&5
```

<img width="1917" height="962" alt="Screenshot 2026-09-30 124720" src="https://github.com/user-attachments/assets/47674e54-25ec-4bfd-aec4-ec2ac059d1ea" />
<img width="1917" height="958" alt="Screenshot 2026-09-30 124706" src="https://github.com/user-attachments/assets/b40848c4-05cb-4fcf-97c7-229d6de5b225" />
<img width="1917" height="971" alt="Screenshot 2026-09-30 124652" src="https://github.com/user-attachments/assets/e151a308-ff77-4aec-8d7c-66bb9074966d" />
<img width="1917" height="967" alt="Screenshot 2026-09-30 124614" src="https://github.com/user-attachments/assets/4cf7d738-bd1c-4835-8f97-59e693ba72d3" />
<img width="1917" height="916" alt="Screenshot 2026-09-30 123526" src="https://github.com/user-attachments/assets/8d7ce0f2-fd1c-453f-ab34-f26856d42d97" />
<img width="1917" height="967" alt="Screenshot 2026-09-30 123250" src="https://github.com/user-attachments/assets/da2e50de-0017-4bf7-bca2-a43806ad692b" />
<img width="1917" height="972" alt="Screenshot 2026-09-30 123159" src="https://github.com/user-attachments/assets/099c8faf-643e-4ba9-a652-e47b72b94d04" />
<img width="1917" height="967" alt="Screenshot 2026-09-30 123016" src="https://github.com/user-attachments/assets/96642386-1f77-49ab-951c-c39da094dd39" />
<img width="1917" height="963" alt="Screenshot 2026-09-30 111939" src="https://github.com/user-attachments/assets/732334a4-ae39-41e6-8b32-6fa7feccd56f" />
<img width="1917" height="962" alt="Screenshot 2026-09-30 111806" src="https://github.com/user-attachments/assets/9fb1dbd7-de89-4aef-b541-b21649ed544a" />
<img width="1917" height="966" alt="Screenshot 2026-09-30 111705" src="https://github.com/user-attachments/assets/3c42a6b5-4e90-413f-a40c-693820492493" />
<img width="1917" height="971" alt="Screenshot 2026-09-30 111537" src="https://github.com/user-attachments/assets/90ea83fb-c964-4934-923e-295f090d78e5" />
<img width="1917" height="970" alt="Screenshot 2026-09-30 111057" src="https://github.com/user-attachments/assets/2d7e2e64-e97e-41ec-b7b6-ffe76abac722" />
<img width="1908" height="982" alt="Screenshot 2026-09-30 110445" src="https://github.com/user-attachments/assets/a38699c1-2a71-4922-ab01-daa1a5c6efb5" />
<img width="1908" height="982" alt="Screenshot 2026-09-30 110445" src="https://github.com/user-attachments/assets/88ee72b5-32bd-49fe-b1f5-3a92f522c625" />
