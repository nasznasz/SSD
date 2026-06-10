# TaskFlow — Secure Task Management System

A secure, OWASP-compliant web application built with **Django 4.2** for the *Secure Software Development (IKB21503)* project. TaskFlow lets users register, log in, and manage their personal tasks, with role-based access control, audit logging, and security controls aligned to the **OWASP Top 10**, **OWASP ASVS**, and **NIST SSDF**.

---

## 1. Project Description

TaskFlow is a task-management web application that demonstrates secure software development practices from the ground up. It implements user authentication, role-based access control (Admin / Normal User), a secure CRUD module for tasks, a user profile page, and an admin-only audit log — all built using a secure framework (Django) and validated through manual code review, dependency scanning, static analysis, and dynamic (penetration) testing.

---

## 2. Features

**Functional**
- User registration & login authentication
- Role-Based Access Control (RBAC): Admin and Normal User
- Secure Task CRUD (create, read, update, delete)
- User profile page
- Admin-only audit log (login attempts & security events)

**Security (OWASP / ASVS)**
| Control | Implementation |
|---|---|
| Input Validation (A03/V5) | Whitelist regex on username & task title; Django forms |
| Authentication & Session (A07/V2) | PBKDF2 hashing, password validators, 15-min idle timeout, session-key rotation |
| Access Control (A01/V4) | `@login_required`, `@admin_required`, owner-scoped queries (no IDOR) |
| Error Handling (V7) | Custom 400/403/404/500 pages; `DEBUG=False` in production |
| Sensitive Data (A02/V3) | Hashed passwords; secrets in `.env`; no secrets logged |
| Configuration (V14) | `.env` for secrets, restricted `ALLOWED_HOSTS`, security headers (X-Frame-Options, nosniff) |
| Logging & Monitoring (V7) | Audit log of logins/denied access; admin-only; read-only |
| Output Encoding (A03/V5) | Django template auto-escaping (no `\|safe` on user data) |
| Injection-free | Django ORM / parameterized queries only — no raw SQL |

---

## 3. Tech Stack & Dependencies

- **Framework:** Django 4.2.30 (Python)
- **Database:** SQLite (default)
- **Config:** django-environ (`.env`)

Full dependency list (`requirements.txt`):
```
asgiref==3.8.1
backports.zoneinfo==0.2.1; python_version < "3.9"
django==4.2.30
django-environ==0.11.2
sqlparse==0.5.5
typing-extensions==4.13.2
tzdata==2026.2
```

---

## 4. Installation

```bash
# 1. Clone the repository
git clone https://github.com/nasznasz/SSD.git
cd SSD

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env from the example
copy .env.example .env        # Windows  (cp on macOS/Linux)
```

Then open `.env` and set a strong secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
Paste the result into `.env`:
```
SECRET_KEY=<paste-the-generated-key-here>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 5. How to Run

```bash
# Apply database migrations
python manage.py migrate

# Create an admin account (becomes Admin role automatically)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser:
- You will be directed to the **login** page — use *Register* to create a normal user account.
- Log in as your **superuser** to access the admin features (Audit Log) and Django admin at **/admin/**.

> For production, set `DEBUG=False` and serve over HTTPS with secure cookie flags enabled.

---

## 6. Project Structure

```
SSD/
├─ core/              # app: models, views, forms, decorators, signals
├─ secure_app/        # project settings, urls, wsgi/asgi
├─ templates/         # base, auth, task, profile, audit, error pages (400/403/404/500)
├─ static/css/        # style.css
├─ docs/              # ZAP scan reports (before/after), evidence
├─ .env.example       # sample environment variables (no real secrets)
├─ .gitignore         # excludes .env, db.sqlite3, venv, __pycache__
├─ requirements.txt   # pinned dependencies
└─ manage.py
```

---

## 7. Security Testing

- **SCA / Dependencies:** `pip-audit -r requirements.txt` → *No known vulnerabilities found*
- **Static Analysis:** `bandit -r core secure_app`
- **Dynamic Testing:** OWASP ZAP active scan — full HTML reports in `docs/zap-report-before.html` and `docs/zap-report-after.html`
- Detailed before/after results are documented in the project technical report.

---

## 8. Screenshots

> Add a screenshot of the running app below (place the image in `docs/screenshots/`):

```
![TaskFlow — My Tasks](docs/screenshots/tasks.png)
![TaskFlow — Login](docs/screenshots/login.png)
```

---

## Author

UniKL MIIT — Secure Software Development (IKB21503), 2025/October.
