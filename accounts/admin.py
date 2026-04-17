from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class PermisoChoiceField(forms.ModelMultipleChoiceField):
    """Muestra solo el nombre del permiso, sin el prefijo app | modelo."""
    def label_from_instance(self, obj):
        return obj.name


class CustomUserChangeForm(forms.ModelForm):
    user_permissions = PermisoChoiceField(
        queryset=Permission.objects.all().select_related('content_type').order_by('name'),
        required=False,
        widget=FilteredSelectMultiple('permisos', is_stacked=False),
        label='Permisos individuales',
    )

    class Meta:
        model = User
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    # Etiquetas en español para los fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': (
                'Marcá "Es staff" para dar acceso al panel de administración. '
                'Asigná permisos individuales según el rol del usuario.'
            ),
        }),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)