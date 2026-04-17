from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

INPUT_CLASS = (
    'flex h-10 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 '
    'text-sm ring-offset-white placeholder:text-zinc-500 '
    'focus-visible:outline-none focus-visible:ring-2 '
    'focus-visible:ring-zinc-950 focus-visible:ring-offset-2'
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'tu@email.com'}),
        label="Correo electrónico"
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Tu nombre'}),
        label="Nombre"
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Tu apellido'}),
        label="Apellido"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': 'nombre_usuario'
        })
        self.fields['username'].label = "Nombre de usuario"
        self.fields['password1'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': '••••••••'
        })
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': '••••••••'
        })
        self.fields['password2'].label = "Confirmar contraseña"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
