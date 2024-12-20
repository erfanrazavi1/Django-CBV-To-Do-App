
from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Task
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin




class TaskListView(LoginRequiredMixin , ListView):
    model = Task
    context_object_name = 'tasks'

    
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView , self).form_valid(form)
    
class EditTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title']
    success_url = '/'

class CompleteTask(LoginRequiredMixin,View):
    model = Task
    success_url = '/'

    def get(self,request,*args,**kwargs):
        object = Task.objects.get(id=kwargs.get('pk'))
        object.complete = True
        object.save()
        return redirect(self.success_url)
    
class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

