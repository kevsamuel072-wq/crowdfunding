from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

# Mapeo de acciones inglés → español
ACCIONES = {
    'Can add':    'Puede agregar',
    'Can change': 'Puede modificar',
    'Can delete': 'Puede eliminar',
    'Can view':   'Puede ver',
}

# Traducciones específicas para mayor claridad
ESPECIFICAS = {
    'Puede agregar log entry':    'Puede agregar entradas de registro',
    'Puede modificar log entry':  'Puede modificar entradas de registro',
    'Puede eliminar log entry':   'Puede eliminar entradas de registro',
    'Puede ver log entry':        'Puede ver entradas de registro',
    'Puede agregar group':        'Puede agregar grupos de usuarios',
    'Puede modificar group':      'Puede modificar grupos de usuarios',
    'Puede eliminar group':       'Puede eliminar grupos de usuarios',
    'Puede ver group':            'Puede ver grupos de usuarios',
    'Puede agregar permission':   'Puede agregar permisos del sistema',
    'Puede modificar permission': 'Puede modificar permisos del sistema',
    'Puede eliminar permission':  'Puede eliminar permisos del sistema',
    'Puede ver permission':       'Puede ver permisos del sistema',
    'Puede agregar user':         'Puede agregar usuarios',
    'Puede modificar user':       'Puede modificar usuarios',
    'Puede eliminar user':        'Puede eliminar usuarios',
    'Puede ver user':             'Puede ver usuarios',
    'Puede agregar content type': 'Puede agregar tipos de contenido',
    'Puede modificar content type': 'Puede modificar tipos de contenido',
    'Puede eliminar content type':  'Puede eliminar tipos de contenido',
    'Puede ver content type':     'Puede ver tipos de contenido',
    'Puede agregar session':      'Puede agregar sesiones',
    'Puede modificar session':    'Puede modificar sesiones',
    'Puede eliminar session':     'Puede eliminar sesiones',
    'Puede ver session':          'Puede ver sesiones',
    'Puede agregar Campaña':      'Puede agregar campañas',
    'Puede modificar Campaña':    'Puede modificar campañas',
    'Puede eliminar Campaña':     'Puede eliminar campañas',
    'Puede ver Campaña':          'Puede ver campañas',
    'Puede agregar Categoría':    'Puede agregar categorías',
    'Puede modificar Categoría':  'Puede modificar categorías',
    'Puede eliminar Categoría':   'Puede eliminar categorías',
    'Puede ver Categoría':        'Puede ver categorías',
    'Puede agregar Donación':     'Puede registrar donaciones',
    'Puede modificar Donación':   'Puede modificar donaciones',
    'Puede eliminar Donación':    'Puede eliminar donaciones',
    'Puede ver Donación':         'Puede ver donaciones',
}


class Command(BaseCommand):
    help = 'Traduce todos los permisos de Django al español'

    def handle(self, *args, **kwargs):
        actualizados = 0

        for permiso in Permission.objects.all():
            nombre_original = permiso.name

            # Paso 1: traducir "Can add/change/delete/view X" → "Puede ... X"
            nombre_nuevo = nombre_original
            for en, es in ACCIONES.items():
                if nombre_original.startswith(en + ' '):
                    objeto = nombre_original[len(en):].strip()
                    nombre_nuevo = f"{es} {objeto}"
                    break

            # Paso 2: aplicar traducción específica si existe
            nombre_nuevo = ESPECIFICAS.get(nombre_nuevo, nombre_nuevo)

            if nombre_nuevo != nombre_original:
                permiso.name = nombre_nuevo
                permiso.save()
                actualizados += 1
                self.stdout.write(f'  {nombre_original}  →  {nombre_nuevo}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ {actualizados} permisos traducidos.'))