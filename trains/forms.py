from django import forms

from cities.models import City
from .models import Train


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Train number', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Input train number',
    }))
    travel_time = forms.IntegerField(label='Travel time (hours)', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Input travel time',
    }))
    from_city = forms.ModelChoiceField(label='From', queryset=City.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    to_city = forms.ModelChoiceField(label='To', queryset=City.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = Train
        fields = ('name', 'travel_time', 'from_city', 'to_city')