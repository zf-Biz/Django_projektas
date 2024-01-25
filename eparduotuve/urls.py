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
    path('profilis/', views.profilis, name='profilis'),
    path('krepseliai/', views.VartotojoKrepselisListView.as_view(), name='mano-krepseliai'),
    path('krepseliai/<int:pk>', views.VartotojoKrepselisDetailView.as_view(), name='mano-krepselis'),
    path('krepseliai/<int:pk>/update', views.KrepselisByUserUpdateView.as_view(), name='krepselis-atnaujinti'),
    path('krepseliai/<int:pk>/eilutes', views.KrepselioEiluteByUserCreateView.as_view(),
         name='eilute-atnaujinti'),
    path('krepseliai/<int:pk>/delete', views.KrepselioEiluteByUserDeleteView.as_view(),
         name='eilute-istrinti'),
    path('krepseliai/<int:pk>/krepselisdelete', views.KrepselisByUserDeleteView.as_view(), name='krepselis-istrinti'),
    path('krepselis/', views.KrepselisByUserCreateView.as_view(), name='krepselis'),

]
