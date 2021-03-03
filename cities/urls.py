from django.urls import path
from . import views


urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.CityListView.as_view(), name='home'),
    path('detail/<int:pk>', views.CityDetailView.as_view(), name='detail'),
    path('add/', views.CityCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.CityDeleteView.as_view(), name='delete'),
]