from bdb import set_trace
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.db.models import Sum
from .models import Lekarz, Inzynier, Sentyment, Opinia, Slowo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from .forms import LekarzRejestracjaForm, InzynierRejestracjaForm, OpiniaForm, LekarzLoginForm, InzynierLoginForm

# Create your views here.

class StronaGlownaView(View):
    template_name = 'strona_glowna.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class LekarzRejestracjaView(CreateView):
    model = Lekarz
    form_class = LekarzRejestracjaForm
    template_name = 'lekarz_rejestracja.html'
    
    def get_success_url(self):
        return reverse('lista_inzynierow')

class InzynierRejestracjaView(CreateView):
    model = Inzynier
    form_class = InzynierRejestracjaForm
    template_name = 'inzynier_rejestracja.html'

    def get_success_url(self):
        return reverse('moje_opinie')

class LekarzLoginView(LoginView):
    template_name = 'lekarz_logowanie.html'
    form_class = LekarzLoginForm
    redirect_authenticated_user = False
   
    def get_success_url(self):
        return reverse('lista_inzynierow')

class InzynierLoginView(LoginView):
    template_name = 'inzynier_logowanie.html'
    form_class = InzynierLoginForm
    redirect_authenticated_user = False
    
    def get_success_url(self):
        return reverse('moje_opinie')
    
class InzynierLogoutView(LogoutView):
    next_page = 'inzynier_logowanie'

class LekarzLogoutView(LogoutView):
    next_page = 'lekarz_logowanie'

@method_decorator(login_required(login_url='lekarz_logowanie'), name='dispatch')
class ListaInzynierowView(View):
    template_name = 'lista_inzynierow.html'

    def get(self, request, *args, **kwargs):
        inzynierowie = Sentyment.objects.values('inzynier').order_by('-total_points')
        print("SQL:", str(inzynierowie.query))

        for i, inzynier in enumerate(inzynierowie, start=1):
            inzynier.rank = i
            print(f"Inżynier {inzynier.inzynier}: Rank={inzynier.rank}, Points={inzynier.total_points}")

        if inzynierowie:
            first_inzynier = inzynierowie[0]
            print(f"First Inzynier: {first_inzynier.inzynier}, Rank: {first_inzynier.rank}, Points: {first_inzynier.total_points}")
        else:
            print("Brak danych dla inżynierów.")

        opinie = Opinia.objects.filter(inzynier__isnull=False)
        print("Opinie przypisane do inżynierów:", opinie)

        return render(request, self.template_name, {'inzynierowie': inzynierowie})
    
@method_decorator(login_required(login_url='inzynier_logowanie'), name='dispatch')
class MojeOpinieView(View):
    template_name = 'moje_opinie.html'

    def get(self, request, *args, **kwargs):
        opinie = Opinia.objects.filter(inzynier=request.user).order_by('-punkty')
        return render(request, self.template_name, {'opinie': opinie})
    
class ZbierzOpinieView(CreateView):
    model = Opinia
    form_class = OpiniaForm
    template_name = 'zbierz_opinie.html'

    def get_success_url(self):
        return '/wynik_opinii/' + str(self.object.pk)

    def form_valid(self, form):
        opinia = form.save()

        if isinstance(self.request.user, Inzynier):
            opinia.inzynier = self.request.user
            sentyment, created = Sentyment.objects.get_or_create(inzynier=self.request.user)
        else:
            pass
        super().form_valid(form)

        opinia.punkty = self.analizuj_sentyment(opinia.tresc)
        opinia.save()

        # Dodaj ten kod, aby mieć pewność, że self.object został ustawiony po zapisaniu formularza
        self.object = opinia

        if isinstance(self.request.user, Inzynier):
            sentyment.total_points += opinia.punkty
            sentyment.save()

        return HttpResponseRedirect(self.get_success_url())
    
    def analizuj_sentyment(self, opinia_text):
        pozytywne_slowa = set(Slowo.objects.filter(jest_pozytywne=True).values_list('slowo', flat=True))

        print("Opinia text:", opinia_text)
        print("Pozytywne słowa:", pozytywne_slowa)

        punkty = sum([1 if slowo in pozytywne_slowa else 0 for slowo in opinia_text.lower().split()])

        print("Punkty:", punkty)
        return punkty
    
class WynikOpiniiView(View):
    template_name = 'wynik_opinii.html'

    def get(self, request, pk, *args, **kwargs):
        opinia = get_object_or_404(Opinia, pk=pk)
        return render(request, self.template_name, {'opinia': opinia})