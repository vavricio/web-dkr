import json

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.views import LoginView as OldLoginView
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from redis import Redis

from .models import AnimeWatching
from .forms import AnimeForm, RegistrationForm

redis = Redis(settings.REDIS_HOST, port=int(settings.REDIS_PORT))


class AnimeCreateView(View):
    def get(self, request):
        if request.user.is_anonymous:
            anime = []
        else:
            anime = AnimeWatching.objects.filter(user=request.user)
        form = AnimeForm()

        return render(request, 'create_instance.html', {
            'form': form.as_p(),
            'anime': anime,
        })

    def post(self, request):
        form = AnimeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')


class AnimeEditView(View):
    def get(self, request, pk):
        cached_anime = redis.get(pk)
        if cached_anime is not None:
            anime = AnimeWatching.from_dict(json.loads(cached_anime))
        else:
            anime = AnimeWatching.objects.get(pk=pk)
            redis.set(pk, json.dumps(anime.as_dict()))

        form = AnimeForm(instance=anime)

        return render(request, 'edit_instance.html', {
            'form': form.as_p(),
        })

    def post(self, request, pk):
        anime = AnimeWatching.objects.get(pk=pk)
        form = AnimeForm(request.POST, instance=anime)

        if form.is_valid():
            form.save()
            redis.delete(pk)
            return HttpResponseRedirect('/')


class AnimeDeleteView(View):
    def post(self, request, pk):
        anime = AnimeWatching.objects.get(pk=pk)
        anime.delete()
        redis.delete(pk)
        return HttpResponseRedirect('/')


class LoginView(OldLoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'

    def get_success_url(self):
        return self.kwargs.get('next', '/')

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return redirect
