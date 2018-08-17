# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='校区', max_length=64, unique=True)),
                ('addr', models.CharField(verbose_name='地址', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_type', models.SmallIntegerField(verbose_name='班级类型', default=0, choices=[(0, '脱产'), (1, '周末班'), (2, '网络班')])),
                ('semester', models.SmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(verbose_name='毕业日期', blank=True, null=True)),
                ('branch', models.ForeignKey(to='crm.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='课程名称', max_length=64, unique=True)),
                ('price', models.PositiveSmallIntegerField(verbose_name='课程价格')),
                ('outline', models.TextField(verbose_name='课程大纲')),
                ('period', models.PositiveSmallIntegerField(verbose_name='课程周期(月)', default=5)),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='课程节次')),
                ('title', models.CharField(verbose_name='本节主题', max_length=64)),
                ('content', models.TextField(verbose_name='本节内容')),
                ('has_homework', models.BooleanField(verbose_name='本节有作业', default=False)),
                ('homework', models.TextField(verbose_name='作业需求', blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('class_grade', models.ForeignKey(verbose_name='上课班级', to='crm.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='跟踪内容')),
                ('status', models.SmallIntegerField(choices=[(0, '近期无报名计划'), (1, '一个月内报名'), (2, '2周内报名'), (3, '已报名')])),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, default=None)),
                ('contact_type', models.SmallIntegerField(default=0, choices=[(0, 'QQ'), (1, '微信'), (2, '手机')])),
                ('contact', models.CharField(max_length=64, unique=True)),
                ('source', models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其他')])),
                ('consult_content', models.TextField(verbose_name='咨询内容')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')])),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_grade', models.ManyToManyField(to='crm.ClassList')),
                ('customer', models.ForeignKey(to='crm.CustomerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('score', models.SmallIntegerField(default=None, choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (75, 'B-'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (0, 'N/A'), (-100, 'COPY')])),
                ('show_status', models.SmallIntegerField(choices=[(0, '缺勤'), (1, '已签到'), (2, '迟到'), (3, '早退')])),
                ('note', models.TextField(verbose_name='成绩备注', blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('course_record', models.ForeignKey(verbose_name='课程', to='crm.CourseRecord')),
                ('student', models.ForeignKey(to='crm.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=64)),
                ('role', models.ManyToManyField(blank=True, to='crm.Role')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='consultant',
            field=models.ForeignKey(verbose_name='课程顾问', to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='refferal_from',
            field=models.ForeignKey(verbose_name='转介绍', blank=True, null=True, to='crm.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='sonsult_courses',
            field=models.ManyToManyField(verbose_name='咨询课程', to='crm.Course'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(to='crm.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='user',
            field=models.ForeignKey(verbose_name='跟进人', to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(verbose_name='讲师', to='crm.UserProfile'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(to='crm.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teacher',
            field=models.ManyToManyField(verbose_name='讲师', to='crm.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together=set([('class_grade', 'day_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('branch', 'course', 'semester')]),
        ),
    ]
