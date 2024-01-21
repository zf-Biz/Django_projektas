from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kategorijos/', views.KategorijaListView.as_view(), name='kategorijos'),
    path('kategorijos/<int:pk>', views.KategorijaDetailView.as_view(), name='kategorija'),
    path('prekes/', views.PrekesListView.as_view(), name='prekes'),
    path('prekes/<int:pk>', views.PrekeDetailView.as_view(), name='preke'),
    path("search/", views.search, name="search"),

    path("register/", views.register_user, name="register"),
]
