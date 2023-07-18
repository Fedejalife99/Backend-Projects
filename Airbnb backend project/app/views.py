from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Reservation, Accommodation
from .forms import new_a, log_in, sign_up
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


@login_required
def new_reservation(request):
    if request.method == "GET":
        return render(request, 'new_reservation.html')
    if request.method == "POST":
        arrival = request.POST.get('arrival')
        departure = request.POST.get('departure')
        # hacer logica para que desde todos los hoteles se pueda hacer la reservacion de cada lugar
        user = request.user
        accommodation = Accommodation.objects.filter(ids=1)
        new_res = Reservation(
            arrival=arrival, departure=departure, accommodations=accommodation, user=user)
        if new_res:
            new_res.save()
            return HttpResponse("your reservation was sucessfully saved")


@login_required
def new_place(request):
    if request.method == "GET":
        return render(request, 'new_place.html', {
            'form': new_a()
        })
    else:
        name = request.POST.get('name')
        price = request.POST.get('price')
        location = request.POST.get('location')
        work_zone = request.POST.get('work_zone') == 'on'
        number_of_rooms = request.POST.get('number_of_rooms')
        number_of_bedrooms = request.POST.get('number_of_bedrooms')
        space_for_people = request.POST.get('space_for_people')
        number_of_stars = request.POST.get('number_of_stars')
        images = request.FILES.get('images')
        user = request.user

        new_hotel = Accommodation(name=name, price=price, location=location, work_zone=work_zone, number_of_rooms=number_of_rooms,
                                  number_of_bedrooms=number_of_bedrooms, space_for_people=space_for_people, number_of_stars=number_of_stars, images=images, user=user)
        print(new_hotel)
        if new_hotel:
            new_hotel.save()
            return HttpResponse("Your place was save")


@login_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {
            'form': sign_up
        })
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(
                username=username, password=password1)
            print(user)
            if user:
                user.save()
                login(request, user)
                return redirect('home')
        return render(request, 'register.html', {
            'form': sign_up,
            'error': "Passwords does not match"
        })


def sign_in(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': log_in
        })
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username=username, password=password1)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'form': log_in,
                'error': "User or password is incorrect"
            })


@login_required
def all_hotel(request):
    if request.method == "GET":
        places = Accommodation.objects.all()
        return render(request, 'all_places.html', {
            'places': places
        })


@login_required
def my_hotels(request):
    if request.method == "GET":
        user = request.user
        places = Accommodation.objects.filter(user=user)
        if len(places) == 0:
            return HttpResponse("You haven't post any place yet")
        return render(request, 'my_places.html', {
            'places': places
        })
    else:
        place_id = request.POST.get('place_id')
        print(place_id)
        place_to_delete = Accommodation.objects.filter(ids=place_id)
        place_to_delete.delete()
        return redirect('my_hotels')


@login_required
def profile(request):
    if request.method == "GET":
        return render(request, 'profile.html')


@login_required
def sign_out(request):
    if request.method == "GET":
        logout(request)
        return redirect('login')
