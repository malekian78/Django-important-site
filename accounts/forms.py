from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
UserModel = get_user_model()
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
    
    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit)
        # user.fullname = self.cleaned_data["fullname"]
        user.is_active = True
        if commit:
            user.save()
        return user
    

class CustomAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """

    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'email',
                "autofocus": True
            }
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": 
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ,
        "inactive": "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )

# ! not work because username field is required
# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(
#         label='Email',
#         widget=forms.TextInput(
#             attrs = {
#                 'placeholder': 'email',
#                 "autofocus": True
#             }
#         )
#     )
    
#     def clean(self):
#         print("******************")
#         self.fields["username"].required = False
#         print(self.fields["username"].__dict__)
#         print("____________________")
#         print(self.fields["email"].__dict__)
#         print("hello")
#         username = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         print("cleaned data:", self.cleaned_data)
#         print("username is ",username)
#         if username is not None and password:
#             self.user_cache = authenticate(
#                 self.request, username=username, password=password
#             )
#             print("user_cashe:",self.user_cache)
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data

#     def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
#         print(user.__dict__)
#         return super().confirm_login_allowed(user)
    

#     # password = forms.CharField(
#     #     label='Password', 
#     #     widget=forms.PasswordInput(
#     #         attrs = {
#     #             'placeholder': 'password'
#     #         }
#     #     )
#     # )
    
