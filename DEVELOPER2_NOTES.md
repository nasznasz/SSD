# Developer 2 — Handoff Notes (Login & Registration, RBAC, Session Security)

This documents the parts I added on top of Developer 1's secure CRUD base.
Use this for the Technical Report (sections 3.2, 3.3, 3.8) and the README.

## 1. Login & Registration  (OWASP ASVS V2 — Authentication)
- `core/forms.py` → `RegistrationForm` (extends Django `UserCreationForm`).
  - Username whitelist regex `^[a-zA-Z0-9_]{3,30}$` (input validation).
  - Unique username + unique email enforced.
  - Passwords are **hashed (PBKDF2)** by Django — never stored in plaintext.
  - Strong-password rules come from `AUTH_PASSWORD_VALIDATORS` (already in settings).
- `core/views.py` → `register()` view; on success it logs the user in
  (which **rotates the session key**, mitigating session fixation).
- Templates: `templates/registration/login.html`, `register.html`,
  shared layout `templates/core/base_auth.html`.
- URLs: `/accounts/register/`, plus Django's built-in `/accounts/login/`
  and `/accounts/logout/`.

## 2. RBAC — Role-Based Access Control  (OWASP ASVS V4 / A5 — Access Control)
- `core/models.py` → `Profile` model with `role` = `admin` | `user`,
  auto-created for every User via a `post_save` signal.
  Superusers are auto-assigned the `admin` role.
- `core/decorators.py` → `@admin_required` decorator. Non-admins get a
  **403 Forbidden** (custom page `templates/403.html`) and the attempt is
  written to the audit log.
- Enforced on the admin-only **Audit Log** page (`/tasks/audit-log/`).
- Navbar (`base.html`) only shows Admin links to admins.

## 3. Session Security  (OWASP ASVS V2 / V3)
Added to `secure_app/settings.py`:
- `SESSION_COOKIE_AGE = 900` (15-minute idle timeout)
- `SESSION_SAVE_EVERY_REQUEST = True` (sliding/idle timeout)
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- `SESSION_COOKIE_HTTPONLY = True` (set by Dev 1) — blocks JS cookie theft
- `SESSION_COOKIE_SAMESITE = 'Lax'` / `CSRF_COOKIE_SAMESITE = 'Lax'`
- Session key is rotated on every login (Django default) — session-fixation safe.
- `*_COOKIE_SECURE` should be set to `True` when deployed over HTTPS.

## 4. Audit Log of Login Attempts  (OWASP ASVS V7 — Logging & Monitoring)
- `core/models.py` → `AuditLog` model (username, action, ip_address,
  user_agent, timestamp). **No passwords / sensitive data stored.**
- `core/signals.py` hooks Django's `user_logged_in`, `user_logged_out`
  and `user_login_failed` signals — every login success/failure/logout
  is recorded automatically.
- Admin-only page at `/tasks/audit-log/` shows the latest 200 events.

## How to run (for the README / demo video)
```bash
python -m venv venv
# Windows: venv\Scripts\activate   |   macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then put a real SECRET_KEY in .env
python manage.py migrate
python manage.py createsuperuser   # this account becomes an Admin
python manage.py runserver
```
Then visit:
- `/accounts/register/` — create a normal user
- `/accounts/login/` — log in
- `/tasks/` — secure CRUD (normal user)
- `/tasks/audit-log/` — admin only (normal users get 403)

## Suggested Git commits (for the "Manages GitHub" part of the demo)
1. `feat(auth): add user registration form and view`
2. `feat(auth): add login/register templates`
3. `feat(rbac): add Profile role model + admin_required decorator`
4. `feat(audit): log login attempts via auth signals + admin audit page`
5. `chore(security): add session timeout settings, .gitignore, .env.example`
