"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', default, name='default'),
    path('add_data/', add_data, name='add_data'),
    path('add_book/', add_book, name='add_book'),
    path('borrow/', borrow, name='borrow'),
    path('get_books/', get_books, name='get_books'),
    path('view/', view, name='view'),
    path('view_borrowers/', view_borrowers, name='view_borrowers'),
    path('receive_book/<int:borrower_id>/', receive_book, name='receive_book')
]