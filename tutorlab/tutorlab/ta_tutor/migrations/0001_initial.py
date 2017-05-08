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
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApptDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_number', models.CharField(max_length=40)),
                ('appt_date', models.CharField(max_length=50)),
                ('old_appt_date', models.CharField(max_length=50, null=True)),
                ('comments', models.CharField(max_length=500)),
                ('student_approved', models.BooleanField(default=True)),
                ('tutor_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.CharField(max_length=50)),
                ('end', models.CharField(max_length=50)),
                ('course', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=500)),
                ('confirmed', models.BooleanField(default=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_date', models.DateTimeField(auto_now_add=True)),
                ('message_title', models.CharField(max_length=100)),
                ('message_content', models.CharField(max_length=2000)),
                ('viewed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionID', models.DateTimeField(auto_now_add=True, null=True)),
                ('student', models.CharField(max_length=6)),
                ('whole_name', models.CharField(max_length=30, null=True)),
                ('classID', models.CharField(max_length=40)),
                ('duration', models.DurationField(max_length=6)),
                ('notes', models.TextField(help_text='Take detailed notes as you help out.')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('classification', models.CharField(default='Freshman', max_length=10)),
                ('about_me', models.TextField(blank=True)),
                ('tutor_type', models.CharField(choices=[('CS', 'CS'), ('MATLAB', 'MATLAB'), ('BOTH', 'BOTH')], default='CS', max_length=6)),
                ('avg_survey_score', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('survey_count', models.IntegerField(default=0)),
                ('token', models.CharField(max_length=150, null=True)),
                ('tutor', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='notification',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='event',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='apptdate',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_tutor.Event'),
        ),
        migrations.AddField(
            model_name='apptdate',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='apptdate',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_tutor.Tutor'),
        ),
    ]
