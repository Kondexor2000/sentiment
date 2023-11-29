"""
URL configuration for sentiment1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from sentimentapp.views import (
    ZbierzOpinieView,
    WynikOpiniiView,
    LekarzRejestracjaView,
    InzynierRejestracjaView,
    LekarzLoginView,
    InzynierLoginView,
    InzynierLogoutView,
    ListaInzynierowView,
    MojeOpinieView,
    LekarzLogoutView,
    StronaGlownaView
)

urlpatterns = [
    path('', StronaGlownaView.as_view(), name='strona_glowna'),
    path('admin/', admin.site.urls),
    path('zbierz_opinie/', ZbierzOpinieView.as_view(), name='zbierz_opinie'),
    path('wynik_opinii/<int:pk>/', WynikOpiniiView.as_view(), name='wynik_opinii'),
    path('lekarz_rejestracja/', LekarzRejestracjaView.as_view(), name='lekarz_rejestracja'),
    path('inzynier_rejestracja/', InzynierRejestracjaView.as_view(), name='inzynier_rejestracja'),
    path('lekarz_logowanie/', LekarzLoginView.as_view(), name='lekarz_logowanie'),
    path('inzynier_logowanie/', InzynierLoginView.as_view(), name='inzynier_logowanie'),
    path('inzynier_wylogowanie/', InzynierLogoutView.as_view(), name='inzynier_wylogowanie'),
    path('lekarz_wylogowanie/', LekarzLogoutView.as_view(), name='lekarz_wylogowanie'),
    path('lista_inzynierow/', ListaInzynierowView.as_view(), name='lista_inzynierow'),
    path('moje_opinie/', MojeOpinieView.as_view(), name='moje_opinie'),
]
