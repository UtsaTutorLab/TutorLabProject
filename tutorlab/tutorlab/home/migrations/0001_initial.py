# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App_Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=40)),
                ('course_number', models.IntegerField(default=0)),
                ('course_section', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CommonStudentIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(max_length=150)),
            ],
        ),
    ]
