


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random
from django.contrib import messages

#### check data is correctly inputed

from models import User,Trip



# Create your views here.


def index(request):
    return redirect('/main')

def main(request):
    return render(request, 'travels/index.html')

def travels(request):
    curr_user = User.objects.get(id = request.session['user_id'])
    joined_trips = Trip.objects.filter(users_joined=curr_user)
    my_trips = Trip.objects.filter(created_by=curr_user)
    other_trips = Trip.objects.exclude(users_joined=curr_user).exclude(created_by=curr_user)
    context = {
        'user' : curr_user,
        'joined_trips': joined_trips,
        'my_trips': my_trips,
        'other_trips': other_trips,
    }

    return render(request, "travels/travels.html", context)

def newtrip(request):
    
    return render(request, "travels/add_trip.html")

def create_trip(request):
    #clean post data
    context = {
        'destination':request.POST.get('destination'),
        'plan':request.POST.get('plan'),
        'start_date':request.POST.get('start_date'),
        'end_date':request.POST.get('end_date'),
    }
    trip_validation_result = Trip.objects.trip_validator(context, request.session['user_id'])
    errors = trip_validation_result[0]
    trip = trip_validation_result[1]

    if bool(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/newtrip')
    return redirect('/travels')

def destination(request, destination_id):
    trip = Trip.objects.get(id=destination_id)
    members = Trip.objects.get(id=destination_id).users_joined.all()
    context = {
        'trip': trip,
        'members': members,
    }
    return render(request, 'travels/destination.html',context)


def join_trip(request, trip_id):
    curr_user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    trip.users_joined.add(curr_user)
    return redirect('/travels')

def new(request):
    return render(request,"travels/create.html")

def create(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        existing = User.objects.filter(email=request.POST['email'])
        if len(existing) > 0:
            errors["email"] = "Email is already in use"

        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            User_1 = User.objects.register_user(request.POST)
            # User_1 = User.objects.get(email=User_1.email)
            request.session['user_id'] = User_1.id
            request.session['login_message'] = "registered!"
            return redirect('/travels')
    # elif request.method =="GET":
    #     return render(request, 'travels/create.html')

def login(request):
    results = User.objects.login_validator(request.POST)
    if len(results[0])>0:
        messages.error(request, results[0]['login'], extra_tags='email')
        return redirect('/')
    User_2 = results[1]
    request.session['user_id'] = User_2.id
    request.session['login_message'] = "Logged in!"
    return redirect('/travels')


def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

