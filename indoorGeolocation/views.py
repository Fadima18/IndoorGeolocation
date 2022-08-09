from enum import unique
from django.shortcuts import render
import folium 
import asyncio, time
import random
from django.http import JsonResponse
from .models import Device, Position
import numpy as np
import datetime
from .fetch_data import room_coordinates
from .forms import RoomForm
import threading

# Create your views here.

def create_indoor_map():
    map_center = (14.794991102571805, -16.965043260134312)
    indoor_map = folium.Map(location=map_center, width = "100%", zoom_start = 22, max_zoom=100)
    pavillon = 'indoorGeolocation/h2.geojson'
    folium.GeoJson(pavillon, name="Pavillon H2").add_to(indoor_map)
    return indoor_map

def render_indoor_map(indoor_map):
    map_html = indoor_map._repr_html_()
    return map_html  

def map_render(request):
    coordinates = list(room_coordinates.values())
    map_center = (14.794991102571805, -16.965043260134312)
    indoor_map = folium.Map(location=map_center, width = "100%", zoom_start = 22, max_zoom=100)
    pavillon = 'indoorGeolocation/h2.geojson'
    folium.GeoJson(pavillon, name="Pavillon H2").add_to(indoor_map)
    
    map_html = indoor_map._repr_html_()
    
    if(request.POST.get('action') == 'post'):
        map_center = (14.794991102571805, -16.965043260134312)
        indoor_map = folium.Map(location = map_center, width = "100%", zoom_start = 22, max_zoom=100)
        folium.GeoJson(pavillon, name="Pavillon H2").add_to(indoor_map)
        position = random.choice(coordinates)
        # position = Position.objects.order_by("-instant")[0]
        new_position = Position(x=position[0], y=position[1], device_id=1)
        new_position.save()
        folium.Marker(location=position).add_to(indoor_map)
        map_html = indoor_map._repr_html_()     
        response = {'map': map_html}
        return JsonResponse(response)
    
    return render(request, 'map.html', {'map': map_html, 'tracking':True})


def track_device(request, id):
    tracked_positions = list()
    indoor_map = create_indoor_map()
    known_positions = list(Position.objects.filter(device_id=id).distinct().values('x', 'y'))
    for position in known_positions:
        new_position = Position.objects.filter(x=position['x'], y=position['y']).latest('instant')
        tracked_positions.append(new_position)
    
    for position in tracked_positions:
        folium.Marker(location=[position.x, position.y], popup= "Last seen here " + str(position.instant)).add_to(indoor_map)
        
    indoor_map_render = render_indoor_map(indoor_map)
    
    return render(request, 'device_tracking.html', {'map': indoor_map_render})   

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
    popular_numbers = np.array(parts)
    popular_numbers.sort()
    popular_numbers = popular_numbers[-1:-4:-1]
    
    place1 = filter(lambda x : True if x == popular_numbers[0] else False, popular_numbers)
    place2 = filter(lambda x : True if x == popular_numbers[1] else False, popular_numbers)
    place3 = filter(lambda x : True if x == popular_numbers[2] else False, popular_numbers)
    
    popular_places = [place1, place2, place3]
            
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