from django.shortcuts import render, HttpResponse, redirect
from apps.loginreg.models import Users
from apps.travels.models import Trips
from django.core.urlresolvers import reverse
from django.db.models import Q

# Create your views here.
def index(request):
    if 'errors' not in request.session:
        request.session['errors'] = 0

    user = Users.objects.get(email=request.session['logged_user'])

    context = {
        'allTravels': Trips.objects.all().exclude(Q(plannedby_user=user.id) | Q(user_joining=user.id)),
        'userTravels': Trips.objects.filter(Q(plannedby_user=user.id) | Q(user_joining=user.id)),
        'users': Users.objects.all(),
    }

    return render(request, 'travels/index.html', context)

def add(request):

    return render(request, 'travels/add.html')

def create(request):
    user = Users.objects.get(email=request.session['logged_user'])

    request.session['errors'] = Trips.objects.addTrip(request.POST, user.id)

    if request.session['errors']['errorsPresent'] is True:
        return redirect(reverse('travels:addTravels'))
    else:
        return redirect(reverse('travels:travelsIndex'))

def destinationView(request, id):
    currentTrip = Trips.objects.get(id=id)
    context = {
        'currentTravel': Trips.objects.get(id=id),
        'planner': Users.objects.get(id=currentTrip.plannedby_user_id),
        'joiningUsers': currentTrip.user_joining.all()
    }

    return render(request, 'travels/view.html', context)

def joinTrip(request, id):
    user = Users.objects.get(email=request.session['logged_user'])
    trip = Trips.objects.get(id=id)

    trip.user_joining.add(user)

    return redirect(reverse('travels:travelsIndex'))