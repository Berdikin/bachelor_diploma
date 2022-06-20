# Generated by Django 3.2.5 on 2022-06-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0003_alter_mark_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='url',
            field=models.URLField(blank=True, max_length=300, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='classroom',
            field=models.CharField(blank=True, help_text='Введите номер аудитории', max_length=10, verbose_name='Аудитория'),
        ),
    ]