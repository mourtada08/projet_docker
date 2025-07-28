from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('statut',)
    search_fields = ('titre', 'description')
