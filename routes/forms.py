from django import forms

from cities.models import City
from trains.models import Train
from .models import Route


class RouteForm(forms.Form):

    from_city = forms.ModelChoiceField(label='From', queryset=City.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control js-select-single'}
    ))
    to_city = forms.ModelChoiceField(label='To', queryset=City.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control js-select-single'}
    ))
    cities = forms.ModelMultipleChoiceField(label='Through cities', queryset=City.objects.all(),
                                            widget=forms.SelectMultiple(attrs={
                                            'class': 'form-control js-select-multiple'}),
                                            required=False)
    total_travel_time = forms.IntegerField(label='Total travel time (hours)', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Input travel time',
    }))


class RouteModelForm(forms.ModelForm):
    name = forms.CharField(label='Route name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Route Name',
    }))
    from_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    to_city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.HiddenInput())
    trains = forms.ModelMultipleChoiceField(queryset=Train.objects.all(),
                                            widget=forms.SelectMultiple(attrs={
                                            'class': 'form-control d-none'}),
                                            required=False)
    total_travel_time = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Route
        fields = '__all__'