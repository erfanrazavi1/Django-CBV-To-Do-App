from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display =['title' , 'complete' , 'created_date' , 'updated_date']
    search_fields = ['title' , 'complete']

    def __str__(self):
        return self.title
    
admin.site.register(Task , TaskAdmin)