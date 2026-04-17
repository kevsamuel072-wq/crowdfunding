from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Donation, Campaign


def _recalcular_monto(campana):
    """Recalcula el monto_recaudado sumando todas las donaciones de la campaña."""
    total = campana.donaciones.aggregate(total=Sum('monto'))['total'] or 0
    Campaign.objects.filter(pk=campana.pk).update(monto_recaudado=total)


@receiver(post_save, sender=Donation)
def actualizar_monto_al_guardar(sender, instance, **kwargs):
    _recalcular_monto(instance.campana)


@receiver(post_delete, sender=Donation)
def actualizar_monto_al_eliminar(sender, instance, **kwargs):
    _recalcular_monto(instance.campana)
