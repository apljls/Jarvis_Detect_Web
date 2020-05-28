from django.conf.urls import url
from django.contrib import admin
from django.urls import path
#from jarvis_detect_web.app.views import *
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('home/', home_page, name='home_page'),
    path('menu/', menu, name='menu'),
    path('opc01/', opc_01, name='opc01'),
    path('opc02/', opc_02, name='opc02'),
    path('opc03/', opc_03, name='opc03'),
    path('opc04/', opc_04, name='opc04'),
    path('opc05/', opc_05, name='opc05'),
    path('opc06/', opc_06, name='opc06'),
    path('opc07/', opc_07, name='opc07'),
    path('result/', result, name='result'),
    path('menu_acesso/', menu_acesso, name='menu_acesso')
]