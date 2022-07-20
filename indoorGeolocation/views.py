from os import sync, times_result
from django.shortcuts import render
import folium 
import asyncio, time
import random
from django.http import JsonResponse
from .models import Device, Position
import numpy as np
import datetime

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
    room_coordinates = {'Tidiane': [14.795032593150454, -16.965048462152478], 
                'Aziz': [14.795003742888513, -16.96504008024931], 
                'Fasou': [14.795038103874212, -16.965012587606907],
                'Assane': [14.794998880484428, -16.96500051766634], 
                'Fallou': [14.795044587078454, -16.964992471039295],
                'Ass': [14.795006984491168, -16.9649800658226],
                'Mor': [14.795058850127111, -16.964958608150482], 
                'Youssou': [14.795032268990242, -16.964949555695057],
                'Empty_room': [14.795066954131599, -16.964938156306744],
                'Bachir': [14.795037455553775, -16.96492776274681],
                'Mounir': [14.795072140694318, -16.964903622865677],
                'Moustapha': [14.795034213951578, -16.964890882372856],
                }
    
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
    
def supervise_place(request, name):
    room_coordinates = {'Tidiane': [14.795032593150454, -16.965048462152478], 
            'Aziz': [14.795003742888513, -16.96504008024931], 
            'Fasou': [14.795038103874212, -16.965012587606907],
            'Assane': [14.794998880484428, -16.96500051766634], 
            'Fallou': [14.795044587078454, -16.964992471039295],
            'Ass': [14.795006984491168, -16.9649800658226],
            'Mor': [14.795058850127111, -16.964958608150482], 
            'Youssou': [14.795032268990242, -16.964949555695057],
            'Empty': [14.795066954131599, -16.964938156306744],
            'Bachir': [14.795037455553775, -16.96492776274681],
            'Mounir': [14.795072140694318, -16.964903622865677],
            'Moustapha': [14.795034213951578, -16.964890882372856],
    }
    
    room = room_coordinates[name.capitalize()]
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
    data = list()
    for label in labels:
        data.append(len(times[times==label]))
    
    # Number of visits for each day for this place
    days_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_data = list()
    for day in days_labels:
        days_data.append(len(days[days==day]))
            
    return render(request, 'places.html', {'data': data, 'labels': labels, 'records': records, 'nom': name, 'today_visits': today_visits, 'days_labels': days_labels, 'days_data': days_data})


# Analytics
def view_analytics(request):
    
    room_coordinates = {'Tidiane': [14.795032593150454, -16.965048462152478], 
        'Aziz': [14.795003742888513, -16.96504008024931], 
        'Fasou': [14.795038103874212, -16.965012587606907],
        'Assane': [14.794998880484428, -16.96500051766634], 
        'Fallou': [14.795044587078454, -16.964992471039295],
        'Ass': [14.795006984491168, -16.9649800658226],
        'Mor': [14.795058850127111, -16.964958608150482], 
        'Youssou': [14.795032268990242, -16.964949555695057],
        'Empty': [14.795066954131599, -16.964938156306744],
        'Bachir': [14.795037455553775, -16.96492776274681],
        'Mounir': [14.795072140694318, -16.964903622865677],
        'Moustapha': [14.795034213951578, -16.964890882372856],
    }
    # Evolution des visites en fonction des jours de la semaine
    visits = list(Position.objects.values('instant'))
        
    dates = [visit['instant'].date() for visit in visits]
    days = [visit['instant'].strftime("%A") for visit in visits]
              
    days = np.array(days)
    days_labels = ["Monday", "Tuesday", "Wednesday", "Thurday", "Friday", "Saturday", "Sunday"]
    days_data = [len(days[days==day]) for day in days_labels]
    
    dates = np.array(dates)
    dates_labels = list(map(lambda x: x.strftime("%d/%m/%Y"), np.unique(dates)))
    dates_data = [len(dates[dates==date]) for date in np.unique(dates)]
    
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today_visits = Position.objects.filter(instant__range=(today_min, today_max)).count()
    
    
    parts = list()
    rooms = list()

    # Camembert
    for room, coordinates in room_coordinates.items():
        parts.append(Position.objects.filter(x=coordinates[0], y=coordinates[1]).count())
        rooms.append(room)  
        
    # Evolution des visites en fonction des jours
    return render(request, 'analytics.html', {'analytics':True, 'days_labels': days_labels, 'days_data': days_data, 'dates_labels': dates_labels, 'dates_data': dates_data, 'today_visits': today_visits, 'rooms': rooms, 'parts': parts})