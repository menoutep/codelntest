from django.urls import path
from . import views
app_name='base'
urlpatterns = [
    path('', views.home, name='home'),
    path('create_model3d/', views.create_model3d, name='create_model3d'),
    path('model_detail/<str:pk>', views.detail_model, name="detail_model"),
]
