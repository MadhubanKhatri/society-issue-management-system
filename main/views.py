from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.contrib import messages

def home(request):
    return render(request,'home.html')


def signup(request):    
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        profession = request.POST['profession']

        if(name!='' or password!='' or phone!='' or city!='' or state!='' or address!=''):
            create_member = Member(name=name, password=password, contact_num=phone, city=city, state=state, 
                                   profession=profession)
            create_member.save()
            messages.success(request,"Member is created successfully.")
        else:
            messages.warning(request,"Please fill all the fields.")
        return redirect('home')



def login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        password = request.POST['password']

        if(user_name!='' or password!=''):
            if Member.objects.filter(name=user_name, password=password).exists():
                return HttpResponse(f'Your welcome {user_name}.')
            else:
                messages.warning(request,"Invalid username or password.")
                return redirect('home')
        else:
            messages.warning(request,"Please fill all the fields.")
            return redirect('home')