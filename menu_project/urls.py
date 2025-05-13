"""
URL configuration for menu_project project.

"""
from django.contrib import admin
from django.urls import path, re_path
from menu_app.views import MenuView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MenuView.as_view(), name='home'),
    path('menu/<str:menu_name>/', MenuView.as_view(), name='menu_by_name'),
    re_path(r'^.*$', MenuView.as_view(), name='fallback'),
]
