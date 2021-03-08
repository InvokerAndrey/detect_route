from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Train
from .forms import TrainForm


class TrainListView(ListView):
    queryset = Train.objects.all()
    paginate_by = 2
    template_name = 'trains/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TrainForm()
        context['form'] = form
        return context


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Train was added'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Train was updated'


class TrainDeleteView(DeleteView):
    model = Train
    success_url = reverse_lazy('trains:home')

    def get(self, request, *args, **kwargs):
        messages.success('Train was deleted')
        return self.post(request, *args, **kwargs)