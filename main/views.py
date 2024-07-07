from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.contrib import messages

def home(request):
    if('username' in request.session):
        session_user = request.session['username']
        member_data = Member.objects.get(name=session_user)
        return render(request, 'welcome.html', {'session_user': request.session['username'], 'member_data': member_data})
    else:
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
        maritial_status = request.POST['maritial_status']
        
        if(name!='' or password!='' or phone!='' or city!='' or state!='' or address!=''):
            create_member = Member(name=name, password=password, contact_num=phone, city=city, state=state, 
                                   profession=profession,maritial_status=maritial_status)
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
                request.session['username'] = user_name
            else:
                messages.warning(request,"Invalid username or password.")
            return redirect('home')
        else:
            messages.warning(request,"Please fill all the fields.")
            return redirect('home')
        

def logout(request):
    if('username' in request.session):
        request.session.flush()
        messages.success(request, 'You are logout successfully.')
    else:
        messages.warning(request, 'You are not logged in.')
    return redirect('home')