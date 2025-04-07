from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from .models import Room, Topic
from .forms import RoomForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) | 
        Q(description__icontains = q) |
        Q(host__username__icontains = q)
        )

    # topics = Topic.objects.all()
    topics = Topic.objects.annotate(room_count=Count('room'))
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # room = Room.objects.get(pk=pk)
    room = get_object_or_404(Room, pk=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    print(request.method)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)
    print(request.method)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form, 'room': room}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'title': room.name}
    return render(request, 'base/delete.html', context)