from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import RouteForm, RouteModelForm
from .utils import get_routes
from cities.models import City
from trains.models import Train
from .models import Route


def home(request):
    form = RouteForm
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as err:
                messages.error(request, err)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Bad trip bitch, we wont get you through it')
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_list = [int(train) for train in trains if train.isdigit()]
            queryset = Train.objects.filter(id__in=trains_list).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk() # in_bulk() делает из qs словарь
            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'total_travel_time': total_time,
                    'trains': queryset,
                }
            )
            context = {'form': form}
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, 'What do ya wanna save?! VOID??')
        return redirect('/')
    
    
def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved your butt')
            return redirect('/')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, 'What do ya wanna save?! VOID??')
        return redirect('/')
    

class RouteListView(ListView):
    model = Route
    paginate_by = 5
    template_name = 'routes/list.html'
    

class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteDeleteView(DeleteView):
    model = Train
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success('Route does not just exist now unlike you')
        return self.post(request, *args, **kwargs)