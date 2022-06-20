# Generated by Django 3.2.5 on 2022-06-11 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0004_auto_20220603_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='name',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Тема занятия'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, max_length=300, null=True, verbose_name='Отзыв')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabinet.timetable', verbose_name='Занятие')),
            ],
        ),
    ]