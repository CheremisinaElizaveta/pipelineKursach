from django import forms
from django.db import transaction
from users.models import User, Role, UserGroup
from django.contrib.auth import authenticate


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    group = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'patronymic', 'group']
        
    def get_role(self):
        role, _ = Role.objects.get_or_create(name='студент')
        return role

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = self.get_role()
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверный логин или пароль')
            self.user = user
        return cleaned_data
    

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "role",
            "group",
            "personality_type",
            "tendencies",
            "personality_recommendations",
            "types_activities",
            "is_banned",
        )


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ("name",)


class GroupForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ("name",)
    