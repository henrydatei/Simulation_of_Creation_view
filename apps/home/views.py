# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db import connections

from apps.home.models import Worlds, Simulations, Creatures, Logs

import numpy as np

def calc_number():
    return 42

def index(request):
    simulations = Simulations.objects.all()
    for sim in simulations:
        sim.number_of_creatures = Creatures.objects.filter(world__simulation=sim.id).count()
        sim.number_of_worlds = Worlds.objects.filter(simulation=sim.id).count()
        sim.number_of_logs = Logs.objects.filter(creature__world__simulation=sim.id).count()
    context = {'segment': 'index', 'simulations': simulations}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def simulation_dashboard(request, simulation_id):
    remaining_food = []
    simulation = get_object_or_404(Simulations, pk=simulation_id)
    
    # get median starting energy for every world
    worlds = Worlds.objects.filter(simulation=simulation_id)
    cursor = connections['default'].cursor()
    cursor.execute("""
        select x.worlds_id, max(x.count_moves) as max_moves 
        from ( 
            SELECT creature_id, count(*) as count_moves, worlds.id as worlds_id 
            FROM logs 
            join creatures 
            on creatures.id = logs.creature_id 
            join worlds 
            on creatures.world_id = worlds.id 
            group by creature_id 
        ) x 
        group by x.worlds_id;
        """)
    max_moves = cursor.fetchall()
    
    # Muss noch angepasst werden
    cursor.execute("""SELECT remaining_food FROM `worlds` ORDER BY `worlds`.`id`;""")
    remaining_foods = cursor.fetchall()
    print("Test")
    print(remaining_foods)
    for food in remaining_foods:
        remaining_food.append(food[0])
    print(remaining_food)
                      
    cursor.close()
    max_moves = {x[0]: x[1] for x in max_moves}
    for world in worlds:
        creatures = Creatures.objects.filter(world=world.id)
        counter = worlds.filter(id__lt=world.id).count()
        if creatures:
            world.median_starting_energy = np.median([creature.start_energy for creature in creatures])
            world.median_sensor_radius = np.median([creature.sensor_radius for creature in creatures])
            world.remaining_food = remaining_food[counter]
            world.maximum_moves = max_moves[world.id]
        else:
            world.median_starting_energy = 0
            world.median_sensor_radius = 0
            world.maximum_moves = 0
            world.remaining_food = 0
    
    context = {'segment': 'simulation_dashboard', 'simulation': simulation, 'worlds': worlds}

    return render(request, 'home/simulation_dashboard.html', context)


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
