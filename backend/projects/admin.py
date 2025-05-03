from django.contrib import admin
from .models import Project, Task

# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'created_by', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('start_date', 'end_date', 'created_by')
    date_hierarchy = 'start_date'
    ordering = ('-created_at',)
    raw_id_fields = ('created_by',)  # Show user as ID dropdown (faster for large datasets)


# Task Admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'assigned_by', 'status', 'priority', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'assigned_to__username', 'assigned_by__username', 'project__title')
    list_filter = ('status', 'priority', 'due_date', 'assigned_to', 'project')
    date_hierarchy = 'due_date'
    ordering = ('-created_at',)
    raw_id_fields = ('project', 'assigned_to', 'assigned_by')  # Dropdown search instead of full select
    list_select_related = ('project', 'assigned_to', 'assigned_by')  # Optimize DB queries
