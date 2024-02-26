from django.db import models
from django.contrib.auth.models import User

class Division(models.Model):
    name = models.CharField(max_length=100, primary_key=True,
                            verbose_name="Название отдела",
                            help_text="Введите название отдела",
                            null=False, blank=False)
    description = models.TextField(verbose_name="Описание отдела")

    def __str__(self):
        return "Отдел: " + self.name

    class Meta:
        db_table = "Отдел"

class Group(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name="Название группы",
                            help_text="Введите название группы",
                            null=False, blank=False)

    def __str__(self):
        return "Группа: " + self.name

    class Meta:
        db_table = "Группа"

class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя",
                                  null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия",
                                 help_text="Введите фамилию",
                                 null=False, blank=False)
    dateOfBirth = models.DateField(verbose_name="Дата рождения",
                                 help_text="Введите дату рождения",
                                 null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                                verbose_name="Группа",
                                help_text="Выберите группу",
                                null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name="id пользователя",
                                help_text="Введите id пользователя",
                                null=True, blank=True)

    def __str__(self):
        return "Имя: " + self.first_name + ", " + "Фамилия: " + self.last_name + ", " + "Группа: " + self.group.__str__()

    class Meta:
        db_table = "Сотрудник"

class Boss(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя",
                                  null=False, blank=False)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия",
                                 help_text="Введите фамилию",
                                 null=False, blank=False)
    dateOfBirth = models.DateField(verbose_name="Дата рождения",
                                 help_text="Введите дату рождения",
                                 null=False, blank=False)
    division = models.ForeignKey(Division, on_delete=models.CASCADE,
                                verbose_name="Отдел",
                                help_text="Выберите отдел",
                                null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name="id пользователя",
                                help_text="Введите id пользователя",
                                null=True, blank=True)

    def __str__(self):
        return "Имя: " + self.first_name + ", " + "Фамилия: " + self.last_name + ", " + "Отдел: " + self.division.__str__()

    class Meta:
        db_table = "Начальник"

class Focus(models.Model):
    focus_name = models.CharField(max_length=100, verbose_name="Направленность",
                                help_text="Введите название направленности", null=False,
                                blank=False, primary_key=True)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE, verbose_name="Начальник",
                                help_text="Выберите начальника",
                                null=False, blank=False)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return "Направленность: " + self.focus_name

    class Meta:
        db_table = "Направленность"

class Assignment(models.Model):
    number = models.IntegerField(verbose_name="Номер задачи",
                                 help_text="Введите номер задачи",
                                 null=False, blank=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 verbose_name="Сотрудник",
                                 help_text="Выберите сотрудника",
                                 null=False, blank=False)
    focus = models.ForeignKey(Focus, on_delete=models.CASCADE,
                                 verbose_name="Направленность",
                                 help_text="Выберите направленность",
                                 null=False, blank=False)
    salary = models.IntegerField(verbose_name="Зарплата",
                                 help_text="Введите размер зарплаты",
                                 null=False, blank=False)
    date_control = models.DateField(verbose_name="Дата сдачи проекта",
                                    help_text="Введите дату сдачи проекта",
                                    null=False, blank=False)

    def __str__(self):
        return "Выполнил: " + self.employee.__str__() + ", " "Зарплата: " + str(self.salary)

    class Meta:
        db_table = "Рабочие задачи"
