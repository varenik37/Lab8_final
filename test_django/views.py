from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from test_django.models import Employee, Assignment, Boss, Focus, Group
from .forms import AssignmentForm
from django.contrib.auth import authenticate


def logout_user(request): # выход из учетной записи
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def show_info(request):  # информация о пользователе
    user = request.user
    print(request.user)
    if user.is_authenticated:
        if user.groups.filter(name="Начальники").exists():
            boss = Boss.objects.get(id_user_id=user.id)
            focuses = list(Focus.objects.filter(boss_id=boss.id))
            return render(request, 'bossView.html', {"focuses": focuses})
        else:
            employee = Employee.objects.get(id_user_id=user.id)
            assignments = list(Assignment.objects.filter(employee=employee.id))
            return render(request, 'EmployeeInfo.html', {"employee": employee, "assignments": assignments})
    else:
        return redirect("")


def show_employee(request, focus_name, id_group, id_user): # информация о сотруднике
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Начальники").exists():
        employee = Employee.objects.get(id_user_id=id_user)
        assignments = list(Assignment.objects.filter(employee=employee.id))
        return render(request, 'EmployeeInfo.html', {"employee": employee,
                                                     "assignments": assignments,
                                                     "focus_name": focus_name,
                                                     "id_group": id_group})
    else:
        return render(request, 'NoAccess.html')


def show_index(request):  # страница регистрации и авторизации
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect('info/')
        else:
            return render(request, 'index.html')
    else:
        if (request.POST.get("email") != None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return redirect("info/")
            except Exception:
                print("Пользователь не найден")
                return redirect("/")
        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_username")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect("info/")


def create_assignment(request, focus_name, id_group, id_user):  # форма создания задачи
    if request.method == "GET":
        form = AssignmentForm()
        return render(request, "FormTemplate.html", {"form": form, "focus_name": focus_name,
                                                     "id_employee":Employee.objects.get(id_user=id_user).id})
    else:
        form_valid = AssignmentForm(request.POST)
        if form_valid.is_valid():
            assignment = form_valid.save(commit=False)
            assignment.employee = Employee.objects.get(id_user_id=id_user)
            assignment.save()
            return redirect(f"/boss/{focus_name}/{id_group}/{id_user}")
        else:
            print("Ошибка!")
            return redirect("/")

def delete_assignment(request, focus_name, id_group, id_user, number_assignment): # удаление задачи
    employee_id = Employee.objects.get(id_user_id=id_user).id
    assignment = Assignment.objects.filter(number=number_assignment, employee_id=employee_id).first().delete()
    return redirect(f"/boss/{focus_name}/{id_group}/{id_user}")


class AssignmentEditView(UpdateView):
    model = Assignment
    fields = ['number', 'date_control', 'salary', 'focus']
    success_url = reverse_lazy('info')
    template_name = 'assignment_confirm_edit.html'


def show_group_ofFocus(request, focus_name): # показывает группу
    focus = Focus.objects.get(focus_name=focus_name)
    groups = focus.groups.filter(focus=focus.focus_name)
    return render(request, 'bossViewGroups.html', {"groups": groups, "focus_name": focus_name})


def show_employee_from_group(request, id_group, focus_name): # показывает сотрудника определенной группы
    employees = Employee.objects.filter(group=Group.objects.get(id=id_group))
    employees_sumAssignments = []
    employee_lastAssignment = []

    for employee in employees:
        employee_assignments = Assignment.objects.filter(employee_id=employee.id)
        sumSalary = sum(map(lambda x: x.salary, employee_assignments))
        employees_sumAssignments.append(sumSalary)
        employee_lastAssignment.append(max(map(lambda x: x.number, employee_assignments)))
        employees = zip(employees, employees_sumAssignments, employee_lastAssignment)

    return render(request, 'bossViewEmployees.html', {
        "employees": employees,
        "lastAssignment": employee_lastAssignment,
        "sumAssignment": employees_sumAssignments,
        "focus_name": focus_name,
        "id_group": id_group
    })

# ajax
def validate_username(request):
    username = request.GET.get('create_username', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)

def check_numberAssignment(request, focus_name, id_employee):
    number = int(request.GET.get('number', None))
    if (number == ""):
        number = 0
    focusObj = Focus.objects.get(focus_name=focus_name)
    response = {
        'exist': Assignment.objects.filter(number__exact=number, focus=focusObj, employee_id=id_employee).exists()
    }
    return JsonResponse(response)
