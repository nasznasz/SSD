# Secure Task Manager — Secure Software Development (IKB 21503)

A secure, microservice-style web application built with **Django**, implementing
secure coding controls aligned with the **OWASP Top 10**, **OWASP ASVS**, and the
**NIST Secure Software Development Framework (SSDF)**.

> Course: Secure Software Development (IKB 21503), UniKL MIIT
> Project: Secure Microservice-Based Web Application with OWASP-Compliant Development Practices

---

## 1. Project Description

Secure Task Manager is a task-management web application that demonstrates secure
software development practices end to end. Users register and log in, are assigned a
role (Admin or Normal User), and manage their own tasks through a secure CRUD module.
All login activity is recorded in an audit log that only admins can view.

The project intentionally applies layered security controls — input validation, secure
authentication and sessions, role-based access control, output encoding, and security
logging — so that the application is resistant to common web attacks such as SQL
injection, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and broken
access control.

---

## 2. Security Features Summary

| Area | Control implemented | OWASP / SSDF |
|------|--------------------|--------------|
| Input Validation | Whitelist regex validation; ORM (no raw SQL) prevents SQL injection | A03 / ASVS V5 / PW.5 |
| Authentication | Custom registration, PBKDF2 password hashing, strong-password validators | A07 / ASVS V2 / PW.5 |
| Session Management | 15-minute idle timeout, HttpOnly + SameSite cookies, session-key rotation on login | ASVS V3 |
| Access Control (RBAC) | Admin / Normal-user roles, `@admin_required` decorator, custom 403 page | A01 / ASVS V4 / PW.5 |
| IDOR Protection | All record queries filtered by owner | A01 / ASVS V4 |
| CSRF Protection | Django CSRF tokens on every state-changing form | ASVS V3 |
| Output Encoding | Django template auto-escaping prevents XSS | A03 / ASVS V5 / PW.5 |
| Sensitive Data | Passwords hashed (never plaintext); secrets kept in `.env` | A02 / PW.4 |
| Logging & Monitoring | Audit log of login success/failure/logout & denied access (no sensitive data) | A09 / ASVS V7 / PW.6 |
| Configuration | `.env` for secrets, `.gitignore` excludes secrets, debug off in production | A05 / PW.6 |

---

## 3. Roles

- **Admin** — full access, including the Audit Log page and the Django admin panel.
  (Any Django superuser is automatically treated as an Admin.)
- **Normal User** — can register, log in, and manage only their own tasks.

---

## 4. Tech Stack & Dependencies

- Python 3.x
- Django 4.2 (LTS)
- django-environ (reads secrets from `.env`)
- SQLite (development database)

Full dependency list: see `requirements.txt`.

---

## 5. Installation

```bash
# 1. Clone the repository
git clone https://github.com/nasznasz/SSD.git
cd SSD

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the .env file from the example, then edit it
#    (set a long random SECRET_KEY)
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
```

Example `.env` contents:

```
SECRET_KEY=replace-with-a-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

> Never commit the real `.env` file. Only `.env.example` (with placeholder values)
> is tracked in Git.

---

## 6. How to Run

```bash
# Apply database migrations
python manage.py migrate

# Create an admin account (this user becomes an Admin automatically)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Then open your browser:

| Page | URL |
|------|-----|
| Register | http://127.0.0.1:8000/accounts/register/ |
| Login | http://127.0.0.1:8000/accounts/login/ |
| My Tasks (secure CRUD) | http://127.0.0.1:8000/tasks/ |
| Audit Log (admin only) | http://127.0.0.1:8000/tasks/audit-log/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

A normal user who tries to open the Audit Log or Django admin is correctly blocked
(custom 403 page / "not authorized").

---

## 7. Project Structure

```
SSD/
├── core/                      # main app
│   ├── models.py              # Task, Profile (RBAC), AuditLog
│   ├── views.py               # registration, CRUD, audit log
│   ├── forms.py               # registration + task validation
│   ├── decorators.py          # @admin_required (access control)
│   ├── signals.py             # login-attempt audit logging
│   ├── admin.py
│   └── migrations/
├── secure_app/                # project settings & URLs
│   ├── settings.py            # security settings (sessions, cookies, etc.)
│   └── urls.py
├── templates/                 # login, register, audit log, CRUD, 403 pages
├── manage.py
├── requirements.txt           # dependency list
├── .env.example               # sample config (no real secrets)
├── .gitignore                 # excludes .env, venv, db, __pycache__
└── README.md
```

---

## 8. Screenshots

> Add screenshots of the running system here, for example:
> - Registration and login pages
> - The task list (secure CRUD)
> - A normal user being blocked from the audit log (403)
> - The admin viewing the audit log

---

## 9. Team Members

| Name | Student ID | GitHub username | Role |
|------|-----------|-----------------|------|
| (fill in) | | | Developer 1 |
| (fill in) | | | Developer 2 |
| (fill in) | | | Report Writer 1 |
| (fill in) | | | Report Writer 2 |
