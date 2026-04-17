from django import forms
from .models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['monto', 'comentario']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': (
                    'flex h-10 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 '
                    'text-sm ring-offset-white placeholder:text-zinc-500 '
                    'focus-visible:outline-none focus-visible:ring-2 '
                    'focus-visible:ring-zinc-950 focus-visible:ring-offset-2'
                ),
                'placeholder': '0.00',
                'min': '1',
                'step': '0.01',
            }),
            'comentario': forms.Textarea(attrs={
                'class': (
                    'flex min-h-[80px] w-full rounded-md border border-zinc-200 bg-white '
                    'px-3 py-2 text-sm ring-offset-white placeholder:text-zinc-500 '
                    'focus-visible:outline-none focus-visible:ring-2 '
                    'focus-visible:ring-zinc-950 focus-visible:ring-offset-2 resize-none'
                ),
                'placeholder': 'Deja un mensaje de apoyo (opcional)...',
                'rows': 3,
            }),
        }
        labels = {
            'monto': 'Monto a donar ($)',
            'comentario': 'Comentario',
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto
