# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('actor_object_id', models.PositiveIntegerField()),
                ('verb', models.CharField(max_length=255)),
                ('target_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.today)),
                ('actor_content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('target_content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True, related_name='target_action_set')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('follower_object_id', models.PositiveIntegerField()),
                ('followee_object_id', models.PositiveIntegerField()),
                ('is_mutual', models.BooleanField(default=False)),
                ('followee_content_type', models.ForeignKey(to='contenttypes.ContentType', related_name='followee_follow_set')),
                ('follower_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('follower_content_type', 'follower_object_id', 'followee_content_type', 'followee_object_id')]),
        ),
    ]
