# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='菜单名字', max_length=64)),
                ('url_type', models.SmallIntegerField(choices=[(0, 'absolute'), (1, 'dynamic')])),
                ('url_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together=set([('name', 'url_name')]),
        ),
        migrations.AddField(
            model_name='role',
            name='menus',
            field=models.ManyToManyField(to='crm.Menus'),
        ),
    ]
