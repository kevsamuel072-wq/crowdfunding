from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        default_permissions = ()
        permissions = [
            ('add_category',    'Puede agregar categorías'),
            ('change_category', 'Puede modificar categorías'),
            ('delete_category', 'Puede eliminar categorías'),
            ('view_category',   'Puede ver categorías'),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Campaign(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='campanas',
        verbose_name="Categoría"
    )
    monto_objetivo = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Monto objetivo ($)"
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de cierre")
    activa = models.BooleanField(default=True, verbose_name="Activa")
    imagen = models.ImageField(
        upload_to='campaigns/', blank=True, null=True, verbose_name="Imagen de portada"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    monto_recaudado = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Monto recaudado ($)"
    )

    class Meta:
        verbose_name = "Campaña"
        verbose_name_plural = "Campañas"
        ordering = ['-created_at']
        default_permissions = ()
        permissions = [
            ('add_campaign',    'Puede agregar campañas'),
            ('change_campaign', 'Puede modificar campañas'),
            ('delete_campaign', 'Puede eliminar campañas'),
            ('view_campaign',   'Puede ver campañas'),
        ]

    def __str__(self):
        return self.titulo

    @property
    def porcentaje_completado(self):
        if self.monto_objetivo <= 0:
            return 0
        porcentaje = (self.monto_recaudado / self.monto_objetivo) * 100
        return min(round(float(porcentaje), 1), 100)

    @property
    def dias_restantes(self):
        from django.utils import timezone
        hoy = timezone.now().date()
        if self.fecha_fin >= hoy:
            return (self.fecha_fin - hoy).days
        return 0

    @property
    def finalizada(self):
        from django.utils import timezone
        return timezone.now().date() > self.fecha_fin


class Donation(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donaciones',
        verbose_name="Usuario"
    )
    campana = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='donaciones',
        verbose_name="Campaña"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto ($)")
    comentario = models.TextField(blank=True, verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = "Donación"
        verbose_name_plural = "Donaciones"
        ordering = ['-created_at']
        default_permissions = ()
        permissions = [
            ('add_donation',    'Puede registrar donaciones'),
            ('change_donation', 'Puede modificar donaciones'),
            ('delete_donation', 'Puede eliminar donaciones'),
            ('view_donation',   'Puede ver donaciones'),
        ]

    def __str__(self):
        return f"{self.usuario.username} → {self.campana.titulo} (${self.monto})"
