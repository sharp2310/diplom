from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from users.models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(forms.ModelForm):
    """Форма для регистрации нового пользователя"""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')  # 'username' убрали

    def clean_password2(self):
        """Проверяет, что пароли совпадают"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        """Сохраняет нового пользователя с хешированным паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Хешируем пароль
        if commit:
            user.save()
        return user

class UserProfileForm(UserChangeForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User  # Указываем модель вашей пользовательской модели
        fields = ('email', 'first_name', 'last_name', 'telegram', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class CustomSetPasswordForm(SetPasswordForm):
    """Форма для смены пароля"""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user


class CustomPasswordResetForm(PasswordResetForm):
    """Форма для сброса пароля"""
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Указанный адрес электронной почты не существует."), code='nonexistent')
        return email