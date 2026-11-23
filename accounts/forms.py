from django import forms

from core.roles import Role


class MockSignInForm(forms.Form):
    """Day 0 only: any email and password are accepted; the role picks which screens you see.
    Day 1 replaces this with Django's AuthenticationForm + django-axes (FR-AUTH-002/003)."""

    email = forms.EmailField(
        error_messages={"required": "Enter your email.", "invalid": "Enter a valid email address."}
    )
    password = forms.CharField(error_messages={"required": "Enter your password."})
    role = forms.ChoiceField(choices=Role.choices, initial=Role.PATIENT)
