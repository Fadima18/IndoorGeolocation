from cgi import test
from turtle import color, position
from venv import create
from django.shortcuts import render
import folium 
import asyncio, time
import random
from django.http import JsonResponse
from .models import Device, Position, Person, Material
import numpy as np
import datetime
from .fetch_data import room_coordinates, compartiments_coordinates
from .forms import RoomForm
import threading

# Create your views here.
        
def style_function(x):
    if(x['geometry']['type'] == 'Polygon'):
        if(x['properties'] == {}):
            return dict({
                'color': '#676767',
                'weight': 2,
                'fillColor': '#676767',
                'fillOpacity': 0.8
            })
        else:
            return dict({
                'color': x['properties']['stroke'],
                'fillColor': x['properties']['fill'],
                'weight': x['properties']['stroke-width'],
                'fillOpacity': x['properties']['fill-opacity']
            })
    elif(x['geometry']['type'] == 'LineString'):
        if(x['properties'] == {}):
            return {
                'color': "#454545",
                'weight': 3
            }
        else: 
            return {
                'color': '#db1b0d',
                'weight': 4,
            }

def create_indoor_map():
    map_center = (14.794991102571805, -16.965043260134312)
    indoor_map = folium.Map(location=map_center, width = "100%", zoom_start = 22, max_zoom=100)
    pavillon = 'indoorGeolocation/h2.geojson'
    folium.GeoJson(pavillon, style_function=style_function).add_to(indoor_map)
    return indoor_map

def map_render(request):
    coordinates = list(room_coordinates.values())
    indoor_map = create_indoor_map()
    
    map_html = indoor_map._repr_html_()
    
    if(request.POST.get('action') == 'post'):
        indoor_map = create_indoor_map()
        position1 = random.choice(coordinates)
        position2 = random.choice(coordinates)
        new_position1 = Position(x=position1[0], y=position1[1], device_id=1)
        new_position2 = Position(x=position2[0], y=position2[1], device_id=2)
        new_position1.save()
        new_position2.save()
        folium.Marker(location=position1, marker_color='red').add_to(indoor_map)
        folium.Marker(location=position2).add_to(indoor_map)
        map_html = indoor_map._repr_html_()     
        response = {'map': map_html}
        return JsonResponse(response)
    
    return render(request, 'map.html', {'map': map_html, 'tracking':True})


def track_material(request):
    coordinates = list(compartiments_coordinates.values())
    indoor_map = create_indoor_map()
    materials = list(Material.objects.all())
    positions = list(random.sample(coordinates, len(materials)))
    
    for material, position in zip(materials, positions):
        folium.Marker(location=position, marker_color='red', popup=material.name).add_to(indoor_map)
    map_html = indoor_map._repr_html_()

    return render(request, 'material_tracking.html', {'map': map_html})

def track_person(request):
    coordinates = list(room_coordinates.values())
    indoor_map = create_indoor_map()
    map_html = indoor_map._repr_html_()
    
    if(request.POST.get('action') == 'post'):
        test_person = Person.objects.get(id=2)
        indoor_map = create_indoor_map()
        position = random.choice(coordinates)
        new_position = Position(x=position[0], y=position[1], device_id=test_person.device.id)
        folium.Marker(location=position).add_to(indoor_map)
        map_html = indoor_map._repr_html_()
        new_position.save()
        response = {'map': map_html}
        return JsonResponse(response)
    
    return render(request, 'person_tracking.html', {'map': map_html})
    
def supervise_place_bis(name):
    room = room_coordinates[name]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    
    # Number of visits in the place named "name" for today
    today_visits = Position.objects.filter(x=room[0], y=room[1], instant__range=(today_min, today_max)).count()
    
    # Number of visits for each hour for this place
    records = list(Position.objects.filter(x=room[0], y=room[1]))
    times = list()
    days = list()
    
    for record in records:
        times.append(record.instant.hour)
        days.append(record.instant.strftime("%A"))
    times = np.array(times)
    days = np.array(days)
    
    labels = list(range(0, 24))
    data = [len(times[times == label]) for label in labels]
    
    # Number of visits for each day for this place
    visits = list(Position.objects.values('instant'))
    
    days_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_data = [len(days[days==day]) for day in days_labels]
    dates = [visit['instant'].date() for visit in visits]
    
    dates = np.array(dates)
    unique_dates = np.unique(dates)
    unique_dates_names = np.array([date.strftime("%A") for date in unique_dates])
    names_count = [len(unique_dates_names[unique_dates_names==day]) for day in days_labels]
    
    days_data = [day_data/name_count if name_count != 0 else day_data for day_data, name_count in zip(days_data, names_count)]
    data = [datum/len(unique_dates) for datum in data]
    
    # Getting the average time that each customer pass in a particular room
    # durations = [] # the list will contain all the durations of the different visits in this particular place
    
    # ## First :  Get all the position objects in this place
    # positions = Position.objects.all().filter(x=room[0], y=room[1]).order_by("-instant")[1:]
    
    # ## Second : For each position, find the moment the corresponding device left
    # for position in positions:
    #     related_device = position.device
    #     related_device_positions = Position.objects.order_by("-instant").filter(device=related_device)
    #     for i in enumerate(related_device_positions):
    #         if(related_device_positions[i] == )
    #     previous_position = 
    
    return {'data': data, 'labels': labels, 'records': records, 'today_visits': today_visits, 'days_labels': days_labels, 'days_data': days_data }

# Analytics
def view_analytics(request):
    # Evolution des visites en fonction des jours de la semaine
    visits = list(Position.objects.values('instant'))
        
    dates = [visit['instant'].date() for visit in visits]
    days = [visit['instant'].strftime("%A") for visit in visits]
              
    days = np.array(days)
    days_labels = ["Monday", "Tuesday", "Wednesday", "Thurday", "Friday", "Saturday", "Sunday"]
        
    days_data = [len(days[days==day]) for day in days_labels]
    
    dates = np.array(dates)
    dates_labels = list(map(lambda x: x.strftime("%d/%m/%Y"), np.unique(dates)))
    unique_dates = np.unique(dates)
    unique_dates_names = np.array([date.strftime("%A") for date in unique_dates])
    names_count = [len(unique_dates_names[unique_dates_names==day]) for day in days_labels]
    dates_data = [len(dates[dates==date]) for date in np.unique(dates)]
    
    days_data = [day_data/name_count if name_count != 0 else day_data for day_data, name_count in zip(days_data, names_count)]
    
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_visits = Position.objects.filter(instant__range=(today_min, today_max)).count()

    # Doughnut 1
    parts = list()
    rooms = list()
    for room, coordinates in room_coordinates.items():
        parts.append(Position.objects.filter(x=coordinates[0], y=coordinates[1]).count())
        rooms.append(room)
        
    # Doughnut 2
    today_parts = list()
    today_rooms = list()
    
    for room, coordinates in room_coordinates.items():
        today_parts.append(Position.objects.filter(x=coordinates[0], y=coordinates[1], instant__range=(today_min, today_max)).count())
        today_rooms.append(room)
        
    # Most popular places
    zipped = list(zip(parts, rooms))
    res = sorted(zipped, key=lambda x: x[0])
    
    popular_places = res[-1:-4:-1]
    
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['room']
            context = supervise_place_bis(name)
            context['places'] = True
            return render(request, 'analytics.html', context)
        
    # Evolution des visites en fonction des jours
    return render(request, 'analytics.html', {'analytics':True, 'places': False, 'days_labels': days_labels, 'days_data': days_data, 'dates_labels': dates_labels, 'dates_data': dates_data, 'today_visits': today_visits, 'rooms': rooms, 'parts': parts, 'today_parts': today_parts, 'today_rooms': today_rooms, 'form': form, 'popular_places': popular_places})