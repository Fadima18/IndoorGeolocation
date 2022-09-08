from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
import folium
import secrets
from django.http import JsonResponse
from .models import Position, Person, Material
import numpy as np
import datetime
from .forms import RoomForm
# Create your views here.


compartiments_coordinates = {
    'Tidiane': [14.795032593150454, -16.965048462152478],
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
    'Khadre': [14.795007956971958, -16.965119540691376],
    'Moussa': [14.794975540943344, -16.965108141303062],
    'Naby': [14.79499628720221, -16.965149044990536],
    'Dieme': [14.79495673964453, -16.96513496339321],
    'Cheikh': [14.794988507355377, -16.965169161558148],
    'Saliou': [14.794948311475569, -16.96515642106533],
    'Elimane': [14.794948959796272, -16.96518927812576],
    'Balla': [14.794981375828854, -16.965199336409565],
    'Malick': [14.79497618926396, -16.965220794081688],
    'Massamba': [14.794943773230601, -16.96521006524563],
    'Kaba': [14.79492367528749, -16.965242251753807],
    'Ameth': [14.794961926209883, -16.965256333351135],
    'Chemin10_A': [14.795071492373983, -16.964921057224274],
    'Chemin10_B': [14.795034862272027, -16.964908987283707],
    'Door10': [14.795092562783811, -16.96492675691843],
    'Chemin9_A': [14.79505560852522, -16.964977383613586],
    'Chemin9_B': [14.795018330100092, -16.964964978396893],
    'Door9': [14.795075058135794, -16.96498341858387],
    'Chemin8_A': [14.795001797926897, -16.96501828730106],
    'Chemin8_B': [14.795001797926897, -16.96501828730106],
    'Door8': [14.795059174287298, -16.96503572165966],
    'Chemin7_A': [14.795005039529578, -16.965134628117085],
    'Chemin7_B': [14.79497035437831, -16.96512322872877],
    'Door7': [14.79502610994587, -16.965140663087368],
    'Chemin6_A': [14.7949875348745, -16.965184584259987],
    'Chemin6_B': [14.794952201399754, -16.965173855423927],
    'Door6': [14.795010550254036, -16.96519162505865],
    'Chemin5_A': [14.794972299340218, -16.965236216783524],
    'Chemin5_B': [14.79493631754225, -16.965225487947464],
    'Door5': [14.794994018080255, -16.965243257582188],
}

room_coordinates = {
    'Chambre5': [14.795050746122305, -16.964914351701736],
    'Chambre6': [14.795036483073138, -16.964970007538795],
    'Chambre7': [14.795019626741068, -16.96502298116684],
    'Chambre8': [14.79498461743184, -16.96512758731842],
    'Chambre9': [14.794969706057682, -16.965179219841954],
    'Chambre10': [14.794952849720433, -16.965229511260983]
}

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
    indoor_map = folium.Map(location=map_center, width="100%", zoom_start=22, max_zoom=100)
    pavillon = 'indoorGeolocation/h2.geojson'
    folium.GeoJson(pavillon, style_function=style_function).add_to(indoor_map)
    return indoor_map


def track_material(request):
    coordinates = list(compartiments_coordinates.values())
    indoor_map = create_indoor_map()
    materials = list(Material.objects.all())
    positions = list(secrets.SystemRandom().sample(coordinates, len(materials)))

    for material, position in zip(materials, positions):
        folium.Marker(location=position, marker_color='red', popup=(material.name)).add_to(indoor_map)
    map_html = indoor_map._repr_html_()

    return render(request, 'material_tracking.html', {'map': map_html, 'material': True})


def track_person(request):
    coordinates = list(room_coordinates.values())
    indoor_map = create_indoor_map()
    map_html = indoor_map._repr_html_()

    print(type(map_html))

    if(request.POST.get('action') == 'post'):
        persons = list(Person.objects.all())
        indoor_map = create_indoor_map()
        for person in persons:
            if(person.device):
                position = secrets.SystemRandom().choice(coordinates)
                new_position = Position(x=position[0], y=position[1], device_id=person.device.id)
                new_position.save()
                folium.Marker(location=position, popup=(person.firstName + " " + person.lastName)).add_to(indoor_map)
        map_html = indoor_map._repr_html_()
        response = {'map': map_html}
        return JsonResponse(response)

    return render(request, 'person_tracking.html', {'map': map_html, 'person': True})


def track_specific_person(request, name):
    coordinates = list(compartiments_coordinates.values())
    indoor_map = create_indoor_map()
    map_html = indoor_map._repr_html_()

    if request.method == 'GET':
        person = Person.objects.filter(firstName__icontains=request.GET.get('name'))[0]
        return render(request, 'specific_person_tracking.html', {'map': map_html, 'name': person.firstName})

    if(request.POST.get('action') == 'post'):
        person = Person.objects.filter(firstName__icontains=name)[0]
        position = secrets.choice(coordinates)
        new_position = Position(x=position[0], y=position[1], device_id=person.device.id)
        new_position.save()
        folium.Marker(location=position, popup=(person.firstName + " " + person.lastName)).add_to(indoor_map)
        map_html = indoor_map._repr_html_()
        response = {'map': map_html, 'person': True}
        return JsonResponse(response)


def track_specific_material(request):
    indoor_map = create_indoor_map()

    if request.method == 'GET':
        material = Material.objects.filter(name__icontains=request.GET.get('name'))[0]
        related_device = material.device
        position = Position.objects.filter(device=related_device).latest('instant')
        location = [position.x, position.y]
        folium.Marker(location=location, popup=(material.name)).add_to(indoor_map)
        map_html = indoor_map._repr_html_()
        return render(request, 'specific_object_tracking.html', {'map': map_html, 'material': True})


def supervise_place_bis(name):
    room = room_coordinates[name]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    today_visits = Position.objects.filter(x=room[0], y=room[1], instant__range=(today_min, today_max)).count()

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

    visits = list(Position.objects.values('instant'))

    days_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_data = [len(days[days == day]) for day in days_labels]
    dates = [visit['instant'].date() for visit in visits]

    dates = np.array(dates)
    unique_dates = np.unique(dates)
    unique_dates_names = np.array([date.strftime("%A") for date in unique_dates])
    names_count = [len(unique_dates_names[unique_dates_names == day]) for day in days_labels]

    days_data = [day_data/name_count if name_count !=
                 0 else day_data for day_data, name_count in zip(days_data, names_count)]
    data = [datum/len(unique_dates) for datum in data]

    return {'data': data, 'labels': labels, 'records': records, 'today_visits': today_visits, 'days_labels': days_labels, 'days_data': days_data}


def view_analytics(request):

    visits = list(Position.objects.values('instant'))

    dates = [visit['instant'].date() for visit in visits]
    days = [visit['instant'].strftime("%A") for visit in visits]

    days = np.array(days)
    days_labels = ["Monday", "Tuesday", "Wednesday", "Thurday", "Friday", "Saturday", "Sunday"]

    days_data = [len(days[days == day]) for day in days_labels]

    dates = np.array(dates)
    dates_labels = list(map(lambda x: x.strftime("%d/%m/%Y"), np.unique(dates)))
    unique_dates = np.unique(dates)
    unique_dates_names = np.array([date.strftime("%A") for date in unique_dates])
    names_count = [len(unique_dates_names[unique_dates_names == day]) for day in days_labels]
    dates_data = [len(dates[dates == date]) for date in np.unique(dates)]

    days_data = [day_data/name_count if name_count !=
                 0 else day_data for day_data, name_count in zip(days_data, names_count)]

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
        today_parts.append(Position.objects.filter(
            x=coordinates[0], y=coordinates[1], instant__range=(today_min, today_max)).count())
        today_rooms.append(room)

    # Most popular places
    zipped = list(zip(parts, rooms))
    res = sorted(zipped, key=lambda x: x[0])

    popular_places = res[-1:-4:-1]

    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        print(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['room']
            context = supervise_place_bis(name)
            context['places'] = True
            return render(request, 'analytics.html', context)

    # Evolution des visites en fonction des jours
    return render(request, 'analytics.html', {'analytics': True, 'places': False, 'days_labels': days_labels, 'days_data': days_data, 'dates_labels': dates_labels, 'dates_data': dates_data, 'today_visits': today_visits, 'rooms': rooms, 'parts': parts, 'today_parts': today_parts, 'today_rooms': today_rooms, 'form': form, 'popular_places': popular_places})
