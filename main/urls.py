from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('ajouter-article/', views.ajouter_article, name="ajouter_article"),
    path('delete_article/<int:id>/', views.delete_article, name="delete_article"),
    path('commande/', views.commande, name="commande"),
    path('orders/<int:id>/', views.orders, name="orders"),
    path('ord/', views.ord, name="ord"),

    # 🔑 Ajoute cette ligne
]
