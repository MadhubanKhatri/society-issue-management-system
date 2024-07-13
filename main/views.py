from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member, Issue
from django.contrib import messages
from django.utils import timezone

def home(request):
    if('username' in request.session):
        session_user = request.session['username']
        member_data = Member.objects.get(name=session_user)
        return render(request, 'welcome.html', {'session_user': request.session['username'], 'member_data': member_data})
    elif('admin_user' in request.session):
        return redirect('dashboard')
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
                                   profession=profession,address=address,marritial_status=maritial_status)
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
            if Member.objects.filter(name=user_name, password=password, isAdmin=False).exists():
                request.session['username'] = user_name
            else:
                messages.warning(request,"Invalid username or password.")
            return redirect('home')
        else:
            messages.warning(request,"Please fill all the fields.")
            return redirect('home')
        

def logout(request, flag):
    if(flag=='IsAdmin'):
        if('admin_user' in request.session):
            del request.session['admin_user']
            messages.success(request, 'You are logout successfully.')
        else:
            messages.warning(request, 'You are not logged in.')
    
    if(flag=='IsUser'):
        if('username' in request.session):
            del request.session['username']
            messages.success(request, 'You are logout successfully.')
        else:
            messages.warning(request, 'You are not logged in.')
    return redirect('home')



def create_issue(request):
    if request.method == 'POST':
        heading = request.POST['heading']
        description = request.POST['description']

        session_user = Member.objects.get(name=request.session['username'])
        
        create_new_issue = Issue(member=session_user, heading=heading, description=description, wing=session_user.wing, 
                                                flat=session_user.flat,status='Raised', pcd=timezone.now())
        create_new_issue.save()
        messages.success(request, 'New issue is raised.')
    return redirect('home')
    

def dashboard(request):
    if('admin_user' in request.session):
        members_issue_details = Issue.objects.all().order_by('-pcd')
        print(members_issue_details)
        data = {'member_issues': members_issue_details}
        return render(request, 'dashboard.html', data)
    else:
        return redirect('home')


def admin_panel_login(request):
    if request.method == 'POST':
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']

        if(admin_username!='' or admin_password!=''):
            if Member.objects.filter(name=admin_username, password=admin_password, isAdmin=True).exists():
                request.session['admin_user'] = admin_username
                return redirect('dashboard')
            else:
                messages.warning(request,"Invalid admin username or password.")
            return redirect('home')
        else:
            messages.warning(request,"Please fill all the fields.")
            return redirect('home')