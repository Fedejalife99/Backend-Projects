from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta, datetime
from django.http import HttpResponseBadRequest, HttpResponse
from .models import Reservation, Accommodation, Califications
from .forms import new_a, log_in, sign_up
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


@login_required
def new_reservation(request):
    """Create a new reservation"""
    if request.method == "GET":
        return render(request, 'new_reservation.html')
    if request.method == "POST":
        arrival_str = request.POST.get('arrival')
        departure_str = request.POST.get('departure')
        place_id = request.session.get('place_id')
        user = request.user
        place = get_object_or_404(Accommodation, ids=place_id)
        all_reserservations = Reservation.objects.filter(
            accommodation_id=place)
        arrival = datetime.strptime(arrival_str, '%Y-%m-%d').date()
        departure = datetime.strptime(departure_str, '%Y-%m-%d').date()
        for reservation in all_reserservations:
            if arrival <= reservation.arrival and departure >= reservation.departure:
                return render(request, 'new_reservation.html', {
                    'error': "This place is already reserved, please choose reserve away from this period {}-{}".format(arrival_str, departure_str)
                })
        new_res = Reservation(
            arrival=arrival, departure=departure, accommodation=place, user=user, accommodation_name=place.name)
        if new_res:
            new_res.save()
            return redirect('myres')
        return HttpResponseBadRequest("something went wrong")


@login_required
def new_place(request):
    """Create a new Hotel"""
    if request.method == "GET":
        return render(request, 'new_place.html', {
            'form': new_a(),
        })
    else:
        name = request.POST.get('name')
        price = request.POST.get('price')
        if int(price) < 0:
            return render(request, 'new_place.html', {
                'form': new_a(),
                'error': "Price must me a positive value"
            })
        location = request.POST.get('location')
        work_zone = request.POST.get('work_zone') == 'on'
        number_of_rooms = request.POST.get('number_of_rooms')
        number_of_bedrooms = request.POST.get('number_of_bedrooms')
        space_for_people = request.POST.get('space_for_people')
        if int(number_of_rooms) < 0 or int(number_of_bedrooms) < 0 or int(space_for_people) < 0:
            return render(request, 'new_place.html', {
                'form': new_a(),
                'error': "Please introduce a valid input"
            })
        images = request.FILES.get('images')
        user = request.user
        if number_of_bedrooms > number_of_rooms:
            return render(request, 'new_place.html', {
                'form': new_a(),
                'error': "Please introduce a valid input"
            })

        new_hotel = Accommodation(name=name, price=price, location=location, work_zone=work_zone, number_of_rooms=number_of_rooms,
                                  number_of_bedrooms=number_of_bedrooms, space_for_people=space_for_people, images=images, user=user)
        if new_hotel:
            new_hotel.save()
            request.session['message'] = "Your place was saved"
            return redirect('my_hotels')


@login_required
def home(request):
    """Home page"""
    return render(request, 'home.html')


def register(request):
    """Register view"""
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
    """Login view"""
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
    """Shows all the hotels"""
    if request.method == "GET":
        places = Accommodation.objects.all()
        for place in places:
            ids = place.ids
            all_califications = Califications.objects.filter(
                accommodation_id=ids)
            total_califications = 0.0
            for calification_obj in all_califications:
                total_califications += calification_obj.calification
            if len(all_califications) > 1:
                average = total_califications / len(all_califications)
                place.calification = round(average, 1)
            else:
                place.calification = round(total_califications, 1)
            place.save()
        return render(request, 'all_places.html', {
            'places': places
        })
    else:
        place_id = request.POST.get('place_id')
        request.session['place_id'] = place_id
        return redirect('newres')


@login_required
def my_hotels(request):
    """Show logged user hotels"""
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
    """User profile"""
    if request.method == "GET":
        return render(request, 'profile.html')


@login_required
def sign_out(request):
    """Logout"""
    if request.method == "GET":
        logout(request)
        return redirect('login')


def my_reservations(request):
    """User reservations"""
    if request.method == "GET":
        user = request.user
        reservations = Reservation.objects.filter(user=user)
        califications = Califications.objects.filter(
            user=user)
        res_with_cal = []
        res_to_cancel = []
        for reservation in reservations:
            for calification in califications:
                if reservation.id == calification.reservation_id:
                    res_with_cal.append(reservation)
                if reservation.arrival > date.today():
                    res_to_cancel.append(reservation)
        print(res_to_cancel)
        return render(request, 'my_reservations.html', {
            'reservations': reservations,
            'res_with_cal': res_with_cal,
            'res_to_cancel': res_to_cancel
        })
    else:
        calification = request.POST.get('Calification')
        accommodation_id = request.POST.get('place_id')
        reservation_id = request.POST.get('reservation_id')
        reservation_obj = Reservation.objects.get(id=reservation_id)
        user = request.user
        review = request.POST.get('review')
        calification_post = Califications.objects.create(
            accommodation_id=accommodation_id, calification=calification, user=user, review=review, reservation=reservation_obj)
        return redirect('myres')


@login_required
def delete_res(request):
    """Delete a reservation"""
    if request.method == "POST":
        res_id = request.POST.get('reservation_id')
        res_to_delete = Reservation.objects.filter(id=res_id).delete()
        return redirect('myres')
