from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from .models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
import requests
import time

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        )  # Filters the queryset to only include objects that belong to the currently authenticated user


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title"]
    success_url = "/"


class CompleteTask(LoginRequiredMixin, View):
    model = Task
    success_url = "/"

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = "/"

    def get(self, request, *args, **kwargs):  # Not showing the confirmation page
        return self.delete(
            request, *args, **kwargs
        )  # automate deleting without confirmation page

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        )  # Filters the queryset to only include objects that belong to the currently authenticated user


class TaskListApiView(TemplateView):
    template_name = "todo/todo_list_api.html"


class CacheWeatherApiView(TemplateView):
    template_name = "todo/todo-weather.html"

    @method_decorator(cache_page(60 * 20))  # Cache for 20 minutes
    @method_decorator(vary_on_cookie)
    @method_decorator(vary_on_headers("User-Agent"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_weather_data(self):
        cache_key = "weather_data"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data
        
        time.sleep(5)  # Simulating delay

        API_KEY = 'ffaed8b527f14f4b409b074d7184d8e7'
        CITY = 'Yasuj'
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_data = {
                'city': CITY,
                'temp': temp,
                'weather': weather,
                'humidity': humidity,
                'wind_speed': wind_speed
            }

            cache.set(cache_key, weather_data, timeout=60 * 20)  # Cache for 20 minutes
            return weather_data
        else:
            return {'error': 'Failed to retrieve weather data'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weather"] = self.get_weather_data()
        return context
