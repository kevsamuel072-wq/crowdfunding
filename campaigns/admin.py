from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Campaign, Donation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'total_campanas', 'created_at')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('created_at',)

    def total_campanas(self, obj):
        return obj.campanas.count()
    total_campanas.short_description = 'Campañas'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'categoria', 'monto_objetivo', 'monto_recaudado',
        'progreso_display', 'activa', 'fecha_fin'
    )
    list_filter = ('activa', 'categoria', 'fecha_inicio', 'fecha_fin')
    search_fields = ('titulo', 'descripcion')
    readonly_fields = ('created_at', 'monto_recaudado')
    list_editable = ('activa',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Información principal', {
            'fields': ('titulo', 'descripcion', 'categoria', 'imagen')
        }),
        ('Financiamiento', {
            'fields': ('monto_objetivo', 'monto_recaudado', 'fecha_inicio', 'fecha_fin', 'activa')
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def progreso_display(self, obj):
        pct = obj.porcentaje_completado
        color = '#22c55e' if pct >= 100 else '#3b82f6' if pct >= 50 else '#f59e0b'
        return format_html(
            '<div style="width:100px;background:#e5e7eb;border-radius:4px;height:10px;">'
            '<div style="width:{}px;background:{};height:10px;border-radius:4px;"></div>'
            '</div> {}%',
            min(pct, 100),
            color,
            pct
        )
    progreso_display.short_description = 'Progreso'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'campana', 'monto', 'created_at')
    list_filter = ('campana', 'created_at')
    search_fields = ('usuario__username', 'campana__titulo', 'comentario')
    readonly_fields = ('created_at',)
    raw_id_fields = ('usuario', 'campana')
