from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list -> lista de itens do modelo


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # Object -> 1 item do modelo

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()  # Salvando a edição da classe no DB
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        usuario.save()
        return super().get(request, *args, **kwargs)  # Redireciona o usuário para a URL final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        busca = self.request.GET.get('query')
        if busca:
            object_list = self.model.objects.filter(titulo__icontains=busca)
            return object_list
        else:
            return None


class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')


class CriarConta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):  # Formulário que cria itens no DB
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')
        # A resposta é o endereço do link em texto e não a view 5por isso o reverse


# ---------->>>>>>>>>> COMO CRIAR FUNCTION BASED VIEWS <<<<<<<<<<---------- #
# Create your views here.
#def homepage(request):
#    return render(request, "homepage.html")


#def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()
#    context['lista_filmes'] = lista_filmes
#    return render(request, "homefilmes.html", context)