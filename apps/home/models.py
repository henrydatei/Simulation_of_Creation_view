# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Creatures(models.Model):
    id = models.IntegerField(primary_key=True)
    start_x = models.IntegerField(blank=True, null=True)
    start_y = models.IntegerField(blank=True, null=True)
    start_energy = models.IntegerField(blank=True, null=True)
    sensor_radius = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    world = models.ForeignKey('Worlds', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creatures'

class Logs(models.Model):
    id = models.IntegerField(primary_key=True)
    creature = models.ForeignKey(Creatures, models.DO_NOTHING, blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    energy = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'

class Simulations(models.Model):
    id = models.IntegerField(primary_key=True)
    world = models.ForeignKey('Worlds', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simulations'

class Worlds(models.Model):
    id = models.IntegerField(primary_key=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    simulation = models.ForeignKey(Simulations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worlds'