from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from test_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name = 'info'),
    path('employee/<int:id_user>/', views.show_employee),
    path('employee/<str:focus_name>/<int:id_group>/<int:id_user>/form/', views.create_assignment, name = "form"),
    path('employee/<str:focus_name>/<int:id_group>/<int:id_user>/<int:number_assignment>/delete/',
         views.delete_assignment, name = "delete_assignment"),
    path('employee/<int:id_user>/form/<int:pk>/edit/', views.AssignmentEditView.as_view(), name='editForm'),
    path('', views.show_index, name = 'home'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name = 'logout'),
    path('user_logout/', views.logout_user, name = 'logout_user'),
    path('boss/<str:focus_name>/', views.show_group_ofFocus, name = 'employee_ofFocus'),
    path('boss/<str:focus_name>/<int:id_group>/', views.show_employee_from_group, name= 'employee_from_group'),
    path('boss/<str:focus_name>/<int:id_group>/<int:id_user>', views.show_employee, name= 'show_employee'),
    #ajax
    path('ajax/validate_username', views.validate_username, name= 'validate_username'),
    path('ajax/check_numberAssignment/<str:focus_name>/<int:id_employee>', views.check_numberAssignment, name= 'check_numberAssignment'),
]

