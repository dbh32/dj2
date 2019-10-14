from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    bs = []
    with open(settings.BUS_STATION_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bs.append({'Name': row['Name'],
                       'Street': row['Street'],
                       'District': row['District']})

    paginator = Paginator(bs, 15)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)
    data = page.object_list

    if page.has_next():
        next_page_url = page.next_page_number()
    else:
        next_page_url = None

    if page.has_previous():
        prev_page_url = page.previous_page_number()
    else:
        prev_page_url = None

    return render_to_response('index.html', context={
        'bus_stations': data,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
