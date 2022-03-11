from email import message
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message, Room
from .forms import RoomForm
from .models import Topic
from .models import Filier 
# Create your views here.
#Login
def LoginPage(request):
    page ='login'
    if request.user.is_authenticated :
        return redirect('home')
    if request.method=='POST':
        password = request.POST.get('password').lower()
        username = request.POST.get('username')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exits')
        
        user = authenticate(request,username=username,password=password)
        if user is not None :
            login(request,user)
            return redirect('home')
        else :
            messages.error(request,'Username or password does not exist')



    context={'page':page,}
    return render(request,'base/login_register.html',context)
    #Logoutd
def logoutPage(request):
    logout(request)
    return redirect('home')
 #Home
def RegisterPage(request):
    if request.user.is_authenticated :
        return redirect('home')
    form = UserCreationForm()
    page='register'
    context={'page':page ,'form':form}
    if request.method == 'POST' :
        form=UserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')

        else :
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',context)
def Home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
            Q(topic__name__icontains=q)|
            Q(name__icontains=q)|
            Q(Description__icontains=q)|
            Q(host__username__icontains=q)
            
            )
    topics = Topic.objects.all()
    rooms_count = rooms.count()

    context = {'rooms':rooms , 'topics':topics , 'rooms_count':rooms_count}
    return render(request,'base/Home.html',context)
#ROOMS
def Rooms(request,pk):
    room = Room.objects.get(id=pk)
    RoomMessages = room.message_set.all().order_by('-created')
    participants = room.participtions.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,room=room
            ,body=request.POST.get('body')
            )
        room.participtions.add(request.user)
        return redirect('Room',pk=room.id)
    
    
    
    context={'room':room ,'RoomMessages':RoomMessages,'participants':participants}
    return render(request,'base/Room.html',context)

    #========================================================
@login_required(login_url='Login')
def CreateRoom(request):
    form =RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context= {'form':form}
    return render(request,'base/RoomForm.html',context)
    #========================

@login_required(login_url='Login')
def UpdateRoom(request,pk):
    
    room = Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are not the user')
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context= {'form':form}
    return render(request,'base/RoomForm.html',context)
    #================================

@login_required(login_url='Login')
def DeleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not the user')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/DeleteForm.html',{'obj':room})
def DeleteMessage(request,pk,pk1):
    message=Message.objects.get(id=pk)
    room=Room.objects.get(id=pk1)
    if request.user != message.user:
        return HttpResponse('You are not the user')
    if request.method == 'POST':
        message.delete()
        messages1 = Message.objects.filter(
            Q(user=request.user)&
            Q(room=room)
            )
        MC=messages1.count()
        if MC == 0:
            room.participtions.remove(request.user)

       
        return redirect('home')
    return render(request,'base/DeleteForm.html',{'obj':message})