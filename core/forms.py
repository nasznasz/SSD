import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task


# ============================================================
#  Developer 2 :  REGISTRATION FORM
# ------------------------------------------------------------
#  Extends Django's UserCreationForm so we keep:
#    - password confirmation
#    - AUTH_PASSWORD_VALIDATORS (strong password rules in settings)
#    - password hashing (PBKDF2 by default - never plaintext)
#  Adds: username whitelist validation + unique email.
#  OWASP ASVS V2 - Authentication
# ============================================================
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Input validation - whitelist only (prevents injection / weird chars)
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
            raise forms.ValidationError(
                "Username must be 3-30 characters and contain only "
                "letters, numbers and underscores."
            )
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


# ============================================================
#  Developer 1 :  Task form  (unchanged)
# ============================================================
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Input validation - no special characters allowed
        if not re.match(r'^[a-zA-Z0-9 _\-]+$', title):
            raise forms.ValidationError(
                "Title can only contain letters, numbers, spaces, hyphens and underscores."
            )
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        # XSS prevention - strip dangerous characters
        if re.search(r'<[^>]*>', description):
            raise forms.ValidationError("HTML tags are not allowed.")
        return description
