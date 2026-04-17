from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django import forms as django_forms
from .forms import RegisterForm

INPUT_CLASS = (
    'flex h-10 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 '
    'text-sm ring-offset-white placeholder:text-zinc-500 '
    'focus-visible:outline-none focus-visible:ring-2 '
    'focus-visible:ring-zinc-950 focus-visible:ring-offset-2'
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido/a a FundIt, {user.first_name or user.username}!")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        form.fields['username'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': 'nombre_usuario'
        })
        form.fields['password'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': '••••••••'
        })
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Hola, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': 'nombre_usuario'
        })
        form.fields['username'].label = "Usuario"
        form.fields['password'].widget.attrs.update({
            'class': INPUT_CLASS, 'placeholder': '••••••••'
        })
        form.fields['password'].label = "Contraseña"

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Sesión cerrada correctamente.")
    return redirect('home')
