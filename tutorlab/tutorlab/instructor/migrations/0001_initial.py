# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 19:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_num', models.CharField(default='N/A', max_length=8)),
                ('course_name', models.CharField(default='N/A', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Course')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.CommonStudentIssue')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=150, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.CharField(max_length=6)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('courses', models.ManyToManyField(to='instructor.Course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='Instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor'),
        ),
    ]