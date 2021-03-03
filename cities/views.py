from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import City
from .forms import CityForm


def home(request, pk=None):
    # Реализация detail_view через функцию
    # if pk:
    #     # city = City.objects.filter(id=pk).first()
    #     city = get_object_or_404(City, id=pk)
    #     return render(request, 'cities/detail.html', {'city': city})
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    form = CityForm()
    cities = City.objects.all()
    paginator = Paginator(cities, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'cities/home.html', context)


class CityListView(ListView):
    queryset = City.objects.all()
    paginate_by = 2
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context


class CityDetailView(DetailView):
    #model = City
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'City was added'


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'City was updated'


class CityDeleteView(DeleteView):
    model = City
    #template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
        # Шоб удалялось без подтверждения
        messages.success(request, 'City was deleted')
        return self.post(request, *args, **kwargs)