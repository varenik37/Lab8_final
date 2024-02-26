from django.contrib import admin
from test_django.models import *

# Register your models here.
#admin.site.register(Division)
#admin.site.register(Employee)
#admin.site.register(Boss)
#admin.site.register(Assignment)
#admin.site.register(Group)
#admin.site.register(Focus)


class FocusInline(admin.TabularInline):
    model = Focus

@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
    def display_group(self):
        return ", ".join([group.name for group in self.groups.all()])

    display_group.short_description = "Группы"
    list_display = ('boss', 'focus_name', display_group)
    list_filter = ('boss',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_filter = ('salary', 'focus', 'number', 'date_control')
    fields = ['employee', ('number', 'salary', 'date_control')]
    list_display = ('employee', 'focus', 'number', 'date_control', 'salary')

@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):
    inlines = [FocusInline]
    list_filter = ('last_name', 'division')
    list_display = ('first_name', 'last_name', 'dateOfBirth', 'division')
    fields = [('first_name', 'last_name'), 'dateOfBirth', 'division']

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ('last_name', 'group')
    list_display = ('first_name', 'last_name', 'dateOfBirth', 'group')
    fields = [('first_name', 'last_name'), 'dateOfBirth', 'group']





