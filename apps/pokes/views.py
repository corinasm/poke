from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

#============================================================#
#                       RENDER METHODS                       #
#============================================================#

def index(request):
    return render (request, 'pokes/index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def pokes (request):
    try: 
        request.session['user_id']
    except KeyError:
        return redirect('/')  

    crt_user = User.objects.get(id=request.session['user_id'])
    other_users = User.objects.all().exclude(id=crt_user.id)

    pokers = crt_user.pokers.all()
    crt_user_pokers_count = pokers.count()
   
    context = {
        'user': crt_user,
        'other_users': other_users,
        'pokers': pokers, 
        'count': crt_user_pokers_count,   
    }
    return render(request, 'pokes/pokes.html', context)

#============================================================#
#                      PROCESS METHODS                       #
#============================================================#


#New User Validation & Registration 
def registration (request):
    # Register a new user 
    if request.method == "POST":

        result = User.objects.validate_registration(request.POST)
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) 
                #print (tag, error_item)

        else:
            request.session['user_id'] = result.id 
            #messages.success(request, 'You have succesfully registered.') 
            return redirect('/pokes')  
 
    return redirect ('/')

def login(request):   

    if request.method == "POST":

        result = User.objects.validate_login(request.POST)
        if type(result) == dict:
            for tag, error_item in result.iteritems():
                messages.error(request, error_item) #using the predifined function error
                #print (tag, error_item)

        else:
            request.session['user_id'] = result.id 
            #messages.success(request, 'You have succesfully logged in.') 
            return redirect('/pokes')  
 
    return redirect ('/')

def poke_user(request, user_id):

    crt_user = User.objects.get(id=request.session['user_id'])
    
    poked_user = User.objects.get(id=user_id)
    poked_user.pokers.add(crt_user)
    poked_user.poke_count += 1
    poked_user.save()

    return redirect ('/pokes')


