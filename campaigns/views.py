from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Category, Campaign, Donation
from .forms import DonationForm


def home(request):
    """Página de inicio con campañas destacadas y categorías."""
    campanas_recientes = Campaign.objects.filter(activa=True).select_related('categoria')[:6]
    categorias = Category.objects.annotate(total=Count('campanas')).order_by('nombre')
    contexto = {
        'campanas_recientes': campanas_recientes,
        'categorias': categorias,
        'total_campanas': Campaign.objects.filter(activa=True).count(),
        'total_donaciones': Donation.objects.count(),
        'total_recaudado': Donation.objects.aggregate(t=Sum('monto'))['t'] or 0,
    }
    return render(request, 'home.html', contexto)


def campaign_list(request):
    """Listado de todas las campañas activas con búsqueda opcional."""
    campanas = Campaign.objects.filter(activa=True).select_related('categoria')
    query = request.GET.get('q', '').strip()
    if query:
        campanas = campanas.filter(titulo__icontains=query)
    categorias = Category.objects.all()
    contexto = {
        'campanas': campanas,
        'categorias': categorias,
        'query': query,
    }
    return render(request, 'campaigns/campaign_list.html', contexto)


def campaigns_by_category(request, slug):
    """Campañas filtradas por categoría."""
    categoria = get_object_or_404(Category, slug=slug)
    campanas = Campaign.objects.filter(categoria=categoria, activa=True)
    categorias = Category.objects.all()
    contexto = {
        'categoria': categoria,
        'campanas': campanas,
        'categorias': categorias,
    }
    return render(request, 'campaigns/campaigns_by_category.html', contexto)


def campaign_detail(request, pk):
    """Detalle de una campaña con su progreso y lista de donaciones."""
    campana = get_object_or_404(Campaign, pk=pk)
    donaciones = campana.donaciones.select_related('usuario').order_by('-created_at')
    ya_dono = (
        request.user.is_authenticated
        and campana.donaciones.filter(usuario=request.user).exists()
    )
    contexto = {
        'campana': campana,
        'donaciones': donaciones,
        'ya_dono': ya_dono,
    }
    return render(request, 'campaigns/campaign_detail.html', contexto)


@login_required
def donate(request, pk):
    """Formulario de donación para usuarios autenticados."""
    campana = get_object_or_404(Campaign, pk=pk, activa=True)

    if campana.finalizada:
        messages.error(request, "Esta campaña ya finalizó y no acepta más donaciones.")
        return redirect('campaign_detail', pk=pk)

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.usuario = request.user
            donacion.campana = campana
            donacion.save()
            messages.success(
                request,
                f"¡Gracias por tu donación de ${donacion.monto} a «{campana.titulo}»!"
            )
            return redirect('campaign_detail', pk=pk)
    else:
        form = DonationForm()

    return render(request, 'campaigns/donate.html', {
        'form': form,
        'campana': campana,
        'amounts': [5, 10, 25, 50],
    })


@login_required
def my_donations(request):
    """Resumen de todas las donaciones del usuario autenticado."""
    donaciones = (
        Donation.objects
        .filter(usuario=request.user)
        .select_related('campana', 'campana__categoria')
        .order_by('-created_at')
    )
    total = donaciones.aggregate(t=Sum('monto'))['t'] or 0
    contexto = {
        'donaciones': donaciones,
        'total': total,
    }
    return render(request, 'campaigns/my_donations.html', contexto)
