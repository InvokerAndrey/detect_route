from django.urls import path
from . import views


urlpatterns = [
    path('', views.TrainListView.as_view(), name='home'),
    path('detail/<int:pk>', views.TrainDetailView.as_view(), name='detail'),
    path('add/', views.TrainCreateView.as_view(), name='create'),
    path('update/<int:pk>', views.TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.TrainDeleteView.as_view(), name='delete'),
]