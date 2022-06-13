from django.shortcuts import render, redirect
from Breath.models import Room, Message
from django.http import HttpResponse, JsonResponse
from Breath.forms import SingUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def cerraseccion(request):
    logout(request)
    return redirect('algo:login')


def iniciarseccion(request):
    if request.user.is_authenticated:
        return redirect('algo:home')
    
    if request.method == 'GET':
        return render(request, 'login.html', {})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error":"No existe"}')
        return redirect('algo:home')


def register(request):
    if request.user.is_authenticated:
        return redirect('algo:home')
    
    
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            
            # print('Register')
            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     print('Existe usuario')
            #     if user.is_active:
            #         print('El usuario esta activo')
            #         login(request, user)
            return redirect('algo:login')
    else:
        form = SingUpForm()

    template = 'register.html'
    context = {'form':form}
    return render(request, template, context)

@login_required(login_url='algo:login')
def home(request):
    
    rooms = Room.objects.all()
    
    current_user = request.user

    context = {'lis_room': rooms, 'user': current_user}
    return render(request, 'inicio.html', context)

@login_required(login_url='algo:login')
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

@login_required(login_url='algo:login')
def room2(request, room, user):
    try:
        room_details = Room.objects.get(name=room)
        return render(request, 'room2.html', {
            'username': user,
            'room': room,
            'room_details': room_details
        })
    except Exception:
        return redirect('algo:home')


# def room(request, room, user):
#     username = request.GET.get('username')
#     room_details = Room.objects.get(name=room)
#     return render(request, 'room.html', {
#         'username': user,
#         'room': room,
#         'room_details': room_details
#     })

@login_required(login_url='algo:login')
def checkview(request):
    room = request.POST['room_name']

    if not Room.objects.filter(name=room).exists():
        new_room = Room.objects.create(name=room)
        new_room.save()

    return redirect('algo:home')

@login_required(login_url='algo:login')
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required(login_url='algo:login')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
