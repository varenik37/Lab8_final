# Generated by Django 4.2.10 on 2024-02-11 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='division',
            field=models.ForeignKey(help_text='Выберите отдел', on_delete=django.db.models.deletion.CASCADE, to='test_django.division', verbose_name='Отдел'),
        ),
    ]
