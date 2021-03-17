from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            queryset = User.objects.filter(username=username)
            if not queryset.exists():
                raise forms.ValidationError("Who are you? We ain't acquainted yet")
            if not check_password(password, queryset[0].password):
                raise forms.ValidationError("Who are you trying to hack up? ")
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("User is not active")
        return super().clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ('username',)

    # Эта джанга ваша оказывается чекает все методы начинаеющиеся на clean...
    def clean_password_confirm(self):
        data = self.cleaned_data
        if data['password'] != data['password_confirm']:
            raise forms.ValidationError('Is it to hard to type password twice correctly?!')
        return data['password']