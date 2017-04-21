from django.shortcuts import render, HttpResponse, redirect
from apps.loginreg.models import Users
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    if 'errors' not in request.session:
        request.session['errors'] = 0


    return render(request, 'loginreg/index.html')

def create(request):
    request.session['errors'] = Users.objects.register(request.POST)

    if request.session['errors']['errorsPresent'] is True:
        return redirect(reverse('login:loginIndex'))
    else:
        request.session['logged_user'] = request.POST['email']
        return redirect(reverse('login:loginSuccess'))

def login(request):
    request.session['errors'] = Users.objects.login(request.POST)


    if request.session['errors']['errorsPresentLogin'] is True:
        return redirect(reverse('login:loginIndex'))
    else:
        request.session['logged_user'] = request.POST['email_login']
        return redirect(reverse('login:loginSuccess'))

def success(request):

    return redirect(reverse('travels:travelsIndex'))

def signOut(request):
    request.session.clear()

    return redirect(reverse('login:loginIndex'))