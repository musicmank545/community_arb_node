from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'api'

urlpatterns = [
    path('<str:apikey>/keys/', views.test, name = 'test'),
    path('<str:apikey>/l2/', views.arb, name = 'arb'),
    path('<str:apikey>/l1/', views.eth, name = 'eth'),
    path('health/', views.health, name = 'health'),
]
