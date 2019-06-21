from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . import models
from .models import User
import bcrypt

def index(request):
    return render(request, 'travel_app/index.html')


def reggy(request): #register validation, adds user to db
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        context = {
            "user_info" : User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashedpw)
        }
        request.session['user_id'] = context['user_info'].id
        return redirect('/dashboard') #redirects to add page

def login(request): #login validation, checks pw/email
    user = User.objects.filter(email = request.POST['email']) #gives back list of dict
    if len(user) < 1:
        messages.error(request, "Invalid login")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        request.session['user_id'] = user[0].id #calling first obj in list
        return redirect('/dashboard') #redirects to add page
    else:
        messages.error(request, "Invalid Login")
        return redirect('/') #returns back to login page

def dashboard(request): #renders home page/dashboard, displays user's trips
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            "user_info": models.User.objects.get(id=request.session['user_id']),
            "trip_info": models.User.objects.get(id=request.session['user_id']).trips.all()
        }
    return render(request, 'travel_app/dashboard.html', context)

def createpage(request, user_id): #renders create page
    context = {
        "user_info": models.User.objects.get(id=user_id)
    }
    print(context['user_info'])
    return render(request, 'travel_app/create.html', context)

def create(request):
    user= User.objects.get(id=request.session['user_id'])
    models.Trip.objects.create(destination = request.POST['destination'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], plan=request.POST['plan'], user=user)
    return redirect ('/dashboard')

def show(request, trip_id):
    context = {
        'trip_info' : models.Trip.objects.get(id=trip_id)
    }
    return render(request, 'travel_app/show.html', context)

def editpage(request, trip_id):
    context= {
        "trip_info" : models.Trip.objects.get(id=trip_id)
    }
    return render(request, 'travel_app/edit.html', context)

def update(request, trip_id):
    print(trip_id)
    update_trip = models.Trip.objects.get(id=int(trip_id))
    update_trip.destination = request.POST['u_destination']
    update_trip.start_date = request.POST['update_start']
    update_trip.start_end = request.POST['update_end']
    update_trip.plan = request.POST['update_description']
    update_trip.save()
    return redirect('/dashboard')

def delete(request, trip_id):
    trip = models.Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect ('/')