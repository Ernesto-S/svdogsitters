from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import json

def redirect_to_svdogsitters(request): # ''
    return redirect('/svdogsitters')

def show_svdogsitters(request): # 'svdogsitters'
    return render(request, 'svdogsitters.html')

def show_registration_form(request): # 'svdogsitters/registration'
    return render(request, 'registration.html')

def register(request): # 'svdogsitters/register'
    if request.method == 'POST':
        errors = Users.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/svdogsitters/registration')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            new_user = Users.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                password=hashed_pw
            )
            request.session['user_id'] = new_user.id
            
            return redirect('/svdogsitters/pet_registration')
    return redirect('/svdogsitters/registration')

def login(request): # 'svdogsitters/login'
    if request.method == 'POST':
        logged_user = Users.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/svdogsitters/welcome')
            else:
                messages.error(request, 'Invalid Password')
                return redirect('/svdogsitters')
        else:
            messages.error(request, 'Invalid Email')
            return redirect('/svdogsitters')
    return redirect('/svdogsitters')

def logout(request): # 'svdogsitters/logout'
    request.session.flush()
    return redirect('/svdogsitters')

def show_pet_registration_form(request): # 'svdogsitters/pet_registration'
    return render(request, 'pet_registration.html')

def pet_register(request): # 'svdogsitters/pet_register'
    if request.method == 'POST':
        errors = Dogs.objects.dog_registration_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/svdogsitters/pet_registration')
        else:
            owner = Users.objects.get(id=request.session['user_id'])
            new_dog = Dogs.objects.create(
                owner=owner,
                dog_name=request.POST['dog_name'],
                dog_birthday=request.POST['dog_birthday'],
                dog_breed=request.POST['dog_breed'],
                dog_weight=request.POST['dog_weight'],
                vet_clinic=request.POST['vet_clinic'],
                vet_address=request.POST['vet_address'],
                vet_phone=request.POST['vet_phone'],
                dog_allergies=request.POST['dog_allergies'],
                dog_comments=request.POST['dog_comments']
            )
            return redirect('/svdogsitters/welcome')
    return redirect('/svdogsitters/pet_registration')

def show_welcome(request): # 'svdogsitters/welcome'
    try:
        if request.session['user_id'] > 0: 
            try:
                if request.session['estimate']:
                    context = {
                        'human': Users.objects.get(id=request.session['user_id']),
                        'estimate': request.session['estimate'],
                        'service_name': request.session['service_name']
                    }
                    return render(request, 'welcome.html', context)
            except:
                context = {
                    'human': Users.objects.get(id=request.session['user_id']),
                    'estimate': 0,
                    'service_name': ''
                }
                return render(request, 'welcome.html', context)
    except:
        return redirect('/svdogsitters')

def request(request): # 'svdogsitters/request'
    if request.method == 'POST':
        request.session['service_name'], service_cost = request.POST["service"].split()

        if service_cost == '35':
            night = int(request.POST["nights"])
            request.session['estimate'] = int(service_cost) * night
        else:
            request.session['estimate'] = service_cost

        requester = Users.objects.get(id=request.session['user_id'])
        new_request = Requests.objects.create(
            requester=requester,
            service=request.session['service_name'],
            estimate=request.session['estimate']
        )
    return redirect('/svdogsitters/welcome')
    #     context = {
    #         'estimate': new_request.estimate,
    #         'service_name': new_request.service
    #     }
    # return HttpResponse(json.dumps(context))

